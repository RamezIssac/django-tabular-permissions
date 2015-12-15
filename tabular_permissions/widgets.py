from __future__ import unicode_literals
import pdb
from django import __version__ as django_version
from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.html import escapejs
from django.utils.safestring import mark_safe
from .app_settings import TABULAR_PERMISSIONS_EXCLUDE_FUNCTION, TABULAR_PERMISSIONS_EXCLUDE_APPS, \
    TABULAR_PERMISSIONS_EXCLUDE_MODELS, TABULAR_PERMISSIONS_TEMPLATE
from .helpers import get_perm_name


class TabularPermissionsWidget(FilteredSelectMultiple):
    class Media:
        js = ('tabular_permissions/tabular_permissions.js',)

    def __init__(self, verbose_name, is_stacked, input_name='user_permissions', attrs=None, choices=()):
        super(TabularPermissionsWidget, self).__init__(verbose_name, is_stacked, attrs, choices)
        self.managed_perms = []
        self.input_name = input_name  # in case of UserAdmin, it's 'user_permissions', GroupAdmin it's 'permissions'
        self.hide_original = True

    def render(self, name, value, attrs=None, choices=()):

        apps_available = []  # main container to send to template
        user_permissions = Permission.objects.filter(id__in=value or []).values_list('id', flat=True)
        all_perms = Permission.objects.all().values('id', 'codename').order_by('codename')
        excluded_perms = []
        codename_id_map = {}
        for p in all_perms:
            codename_id_map[p['codename']] = p['id']

        reminder_perms = codename_id_map.copy()
        # used to detect if the tabular permissions covers all permissions, if so, we don't need to make it visible.

        for app in apps.get_app_configs():
            app_dict = {'verbose_name': force_text(app.verbose_name),
                        'models': []}

            for model_name in app.models:
                model = app.models[model_name]

                add_perm_name = get_perm_name(model_name, 'add')
                change_perm_name = get_perm_name(model_name, 'change')
                delete_perm_name = get_perm_name(model_name, 'delete')

                add_perm_id = codename_id_map.get(add_perm_name, False)
                change_perm_id = codename_id_map.get(change_perm_name, False)
                delete_perm_id = codename_id_map.get(delete_perm_name, False)

                if add_perm_id and change_perm_id and delete_perm_id:

                    if app.label in TABULAR_PERMISSIONS_EXCLUDE_APPS \
                            or model_name in TABULAR_PERMISSIONS_EXCLUDE_MODELS \
                            or TABULAR_PERMISSIONS_EXCLUDE_FUNCTION(model):

                        excluded_perms.extend([add_perm_id, change_perm_id, delete_perm_id])
                        reminder_perms.pop(add_perm_name)
                        reminder_perms.pop(change_perm_name)
                        reminder_perms.pop(delete_perm_name)
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
                    excluded_perms.extend([add_perm_id, change_perm_id, delete_perm_id])
                    reminder_perms.pop(add_perm_name)
                    reminder_perms.pop(change_perm_name)
                    reminder_perms.pop(delete_perm_name)

            if app.models:
                apps_available.append(app_dict)

        request_context = {'apps_available': apps_available, 'user_permissions': user_permissions,
                           'codename_id_map': codename_id_map, 'input_name': self.input_name}
        body = get_template(TABULAR_PERMISSIONS_TEMPLATE).render(request_context).encode("utf-8")
        self.managed_perms = excluded_perms
        if reminder_perms:
            self.hide_original = False

        # Get "original" FilteredSelectMultiple, and hide it if necessary.
        # Next block is a "copy" of FilteredSelectMultiple render(), except the if reminder_perms: check.
        # Due to change in how SelectFilter take its arguments and the dropping of static('admin/') in django1.9
        # there a check on django version

        if attrs is None:
            attrs = {}
        attrs['class'] = 'selectfilter'
        if self.is_stacked:
            attrs['class'] += 'stacked'

        output = [super(FilteredSelectMultiple, self).render(name, value, attrs, choices)]
        if reminder_perms:
            output.append('<script type="text/javascript">addEvent(window, "load", function(e) {')

            if django_version == '1.8':
                output.append('SelectFilter.init("id_%s", "%s", %s, "%s"); });</script>\n'
                              % (name, self.verbose_name.replace('"', '\\"'), int(self.is_stacked), static('admin/')))
            else:  # 1.9
                output.append('SelectFilter.init("id_%s", "%s", %s); });</script>\n'
                              % (name, escapejs(self.verbose_name), int(self.is_stacked)))

        initial = mark_safe(''.join(output))
        response = ' <hr/>'.join([force_text(body), force_text(initial)])
        return mark_safe(response)

    def render_option(self, selected_choices, option_value, option_label):
        if option_value in self.managed_perms:
            # permission is covered in table, skip it.
            return ''
        self.hide_original = False
        return super(TabularPermissionsWidget, self).render_option(selected_choices, option_value, option_label)

    def build_attrs(self, extra_attrs=None, **kwargs):
        if self.hide_original:
            extra_attrs['style'] = " display:none "
        return super(TabularPermissionsWidget, self).build_attrs(extra_attrs, **kwargs)
