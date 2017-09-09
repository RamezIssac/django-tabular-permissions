from __future__ import unicode_literals
from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.contenttypes.models import ContentType
from django.forms import SelectMultiple
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from .app_settings import TABULAR_PERMISSIONS_EXCLUDE_FUNCTION, TABULAR_PERMISSIONS_EXCLUDE_APPS, \
    TABULAR_PERMISSIONS_EXCLUDE_MODELS, TABULAR_PERMISSIONS_TEMPLATE, TABULAR_PERMISSIONS_USE_FOR_CONCRETE
from .helpers import get_perm_name

def get_reminder_permissions_iterator(choices, reminder_perms):
    reminder_perms_list = reminder_perms.values()
    l = []
    for c in choices:
        if c[0] in reminder_perms_list:
            l.append(c)
    return l


class TabularPermissionsWidget(FilteredSelectMultiple):
    class Media:
        js = ('tabular_permissions/tabular_permissions.js',)

    def __init__(self, verbose_name, is_stacked, input_name='user_permissions', attrs=None, choices=()):
        super(TabularPermissionsWidget, self).__init__(verbose_name, is_stacked, attrs, choices)
        self.managed_perms = []
        self.input_name = input_name  # in case of UserAdmin, it's 'user_permissions', GroupAdmin it's 'permissions'
        self.hide_original = True

    def render(self, name, value, attrs=None, renderer=None):
        choices = self.choices
        apps_available = []  # main container to send to template
        user_permissions = Permission.objects.filter(id__in=value or []).values_list('id', flat=True)
        all_perms = Permission.objects.all().values('id', 'codename', 'content_type_id').order_by('codename')
        excluded_perms = set([])
        codename_id_map = {}
        for p in all_perms:
            codename_id_map['%s_%s' % (p['codename'], p['content_type_id'])] = p['id']

        reminder_perms = codename_id_map.copy()
        # used to detect if the tabular permissions covers all permissions, if so, we don't need to make it visible.

        for app in apps.get_app_configs():
            app_dict = {'verbose_name': force_text(app.verbose_name),
                        'models': []}

            for model_name in app.models:
                model = app.models[model_name]
                ct_id = ContentType.objects.get_for_model(model, for_concrete_model=TABULAR_PERMISSIONS_USE_FOR_CONCRETE).pk
                add_perm_name = get_perm_name(model_name, 'add')
                change_perm_name = get_perm_name(model_name, 'change')
                delete_perm_name = get_perm_name(model_name, 'delete')
                add_perm_id = codename_id_map.get('%s_%s' % (add_perm_name, ct_id), False)
                change_perm_id = codename_id_map.get('%s_%s' % (change_perm_name, ct_id), False)
                delete_perm_id = codename_id_map.get('%s_%s' % (delete_perm_name, ct_id), False)

                if add_perm_id and change_perm_id and delete_perm_id and not {add_perm_id, change_perm_id,
                                                                              delete_perm_id} & excluded_perms:
                    excluded_perms.update([add_perm_id, change_perm_id, delete_perm_id])
                    reminder_perms.pop('%s_%s' % (add_perm_name, ct_id))
                    reminder_perms.pop('%s_%s' % (change_perm_name, ct_id))
                    reminder_perms.pop('%s_%s' % (delete_perm_name, ct_id))

                    if app.label in TABULAR_PERMISSIONS_EXCLUDE_APPS \
                            or model_name in TABULAR_PERMISSIONS_EXCLUDE_MODELS \
                            or TABULAR_PERMISSIONS_EXCLUDE_FUNCTION()(model):
                        continue

                    app_dict['models'].append({
                        'model_name': model_name,
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

            if app.models:
                apps_available.append(app_dict)

        request_context = {'apps_available': apps_available, 'user_permissions': user_permissions,
                           'codename_id_map': codename_id_map, 'input_name': self.input_name}
        body = get_template(TABULAR_PERMISSIONS_TEMPLATE).render(request_context).encode("utf-8")
        self.managed_perms = excluded_perms
        if reminder_perms:
            self.hide_original = False

        reminder_choices = get_reminder_permissions_iterator(choices, reminder_perms)
        if not reminder_choices:
            attrs['style'] = " display:none "
            # switching to "normal" SelectMultiple as FilteredSelectMultiple will render the widget even
            # if the style=display:none
            original_class = SelectMultiple(attrs, reminder_choices)
        else:
            original_class = FilteredSelectMultiple(self.verbose_name, self.is_stacked, attrs, reminder_choices)

        output = original_class.render(name, value, attrs, renderer)

        initial = mark_safe(''.join(output))
        response = ' <hr/>'.join([force_text(body), force_text(initial)])
        return mark_safe(response)
