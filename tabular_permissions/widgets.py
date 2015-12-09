from django.contrib.auth.models import Permission
from django.forms import SelectMultiple
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.apps import apps


class TabularPermissions(SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        # First we construct a list of dicts to hold apps and their models
        # we need to know all custom permissions available
        permissions_available = [u'add', u'change', u'delete']
        apps_available = []
        user_permissions = Permission.objects.filter(id__in=value).values_list('codename', flat=True)
        all_perms = Permission.objects.all().values('id', 'codename').order_by('codename')
        perm_ids = []
        perm_names = []
        codename_id_map = {}
        for p in all_perms:
            codename_id_map[p['codename']] = p['id']
            # perm_ids.append(p['id'])
            # perm_names.append(p['codename'])

        for app in apps.get_app_configs():
            app_dict = {'verbose_name': force_text(app.verbose_name),
                        'models': []}
            for model_name in app.models:
                model = app.models[model_name]
                app_dict['models'].append({
                    'model': model,
                    'verbose_name': force_text(model._meta.verbose_name_plural)
                })
            if app.models:
                apps_available.append(app_dict)


        # rener the template
        request_context = {'apps_available': apps_available, 'user_permissions': user_permissions,
                           'codename_id_map': codename_id_map}
        body = get_template('admin/tabular_permissions.html').render(request_context).encode("utf-8")
        # pdb.set_trace()
        # attrs['style'] = 'display:none;'
        initial = super(TabularPermissions, self).render(name, value, attrs, choices)
        response = u'%s <hr> %s' % (force_text(body), force_text(initial))
        return mark_safe(response)
