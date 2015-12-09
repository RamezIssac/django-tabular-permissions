from __future__ import unicode_literals
from django.contrib.auth.models import Permission
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.apps import apps
from . import app_settings
from .helpers import get_perm_name


class TabularPermissions(FilteredSelectMultiple):
    def __init__(self, verbose_name, is_stacked, attrs=None, choices=()):
        super(TabularPermissions, self).__init__(verbose_name, is_stacked, attrs, choices)
        self.exclude_perms = []

    def render(self, name, value, attrs=None, choices=()):
        # First we construct a list of dicts to hold apps and their models
        # we need to know all custom permissions available

        apps_available = []
        user_permissions = Permission.objects.filter(id__in=value).values_list('id', flat=True)
        all_perms = Permission.objects.all().values('id', 'codename').order_by('codename')
        excluded_perms = []
        codename_id_map = {}
        for p in all_perms:
            codename_id_map[p['codename']] = p['id']
            # perm_ids.append(p['id'])
            # perm_names.append(p['codename'])

        for app in apps.get_app_configs():
            app_dict = {'verbose_name': force_text(app.verbose_name),
                        'models': []}

            for model_name in app.models:
                add_perm_name = get_perm_name(model_name, 'add')
                change_perm_name = get_perm_name(model_name, 'change')
                delete_perm_name = get_perm_name(model_name, 'delete')

                add_perm_id = codename_id_map.get(add_perm_name, False)
                change_perm_id = codename_id_map.get(change_perm_name, False)
                delete_perm_id = codename_id_map.get(delete_perm_name, False)

                if app.label in app_settings.TABULAR_PERMISSIONS_EXCLUDE_APPS \
                        or model_name in app_settings.TABULAR_PERMISSIONS_EXCLUDE_MODELS:
                    excluded_perms.extend([add_perm_id, change_perm_id, delete_perm_id])
                    continue

                if add_perm_id and change_perm_id and delete_perm_id:
                    model = app.models[model_name]
                    app_dict['models'].append({
                        'model': model,
                        'verbose_name_plural': force_text(model._meta.verbose_name_plural),
                        'verbose_name': force_text(model._meta.verbose_name),
                        'add_perm_id': add_perm_id,
                        'add_perm_name': add_perm_name,
                        'change_perm_id': change_perm_id,
                        'change_perm_name': change_perm_name,
                        'delete_perm_id': delete_perm_id,
                        'delete_perm_name': delete_perm_name,
                    })
                    excluded_perms.extend([add_perm_id, change_perm_id, delete_perm_id])

            if app.models:
                apps_available.append(app_dict)

        request_context = {'apps_available': apps_available, 'user_permissions': user_permissions,
                           'codename_id_map': codename_id_map}
        body = get_template(app_settings.TABULAR_PERMISSIONS_TEMPLATE).render(request_context).encode("utf-8")
        self.exclude_perms = excluded_perms
        # pdb.set_trace()
        # attrs['style'] = 'display:none;'
        initial = super(TabularPermissions, self).render(name, value, attrs, choices)
        response = u'%s <hr> %s' % (force_text(body), force_text(initial))
        return mark_safe(response)

    def render_option(self, selected_choices, option_value, option_label):
        if option_value in self.exclude_perms:
            return ''
        return super(TabularPermissions, self).render_option(selected_choices, option_value, option_label)
