from django.contrib import admin

from django.contrib.auth.admin import UserAdmin, User
from django.core.exceptions import ImproperlyConfigured
from tabular_permissions.widgets import TabularPermissions


class TabularPermissionsUserAdmin(UserAdmin):
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        field = super(TabularPermissionsUserAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'user_permissions':
            field.widget = TabularPermissions(db_field.verbose_name, db_field.name in self.filter_vertical)
            field.help_text = ''
        return field

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # pdb.set_trace()
        print request.POST
        return super(TabularPermissionsUserAdmin, self).change_view(request, object_id, form_url, extra_context)


try:
    admin.site.unregister(User)
    admin.site.register(User, TabularPermissionsUserAdmin)
except:
    raise ImproperlyConfigured('Please put django.contrib.auth before tabular_permissions in INSTALLED_APPS')
