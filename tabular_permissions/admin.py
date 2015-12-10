from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, User, Group, GroupAdmin
from django.core.exceptions import ImproperlyConfigured
from tabular_permissions.widgets import TabularPermissionsWidget
from . import app_settings


class UserTabularPermissionsAdminBase(object):
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        field = super(UserTabularPermissionsAdminBase, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'user_permissions':
            field.widget = TabularPermissionsWidget(db_field.verbose_name, db_field.name in self.filter_vertical)
            field.help_text = ''
        return field


class GroupTabularPermissionsAdminBase(object):
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        field = super(GroupTabularPermissionsAdminBase, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'permissions':
            field.widget = TabularPermissionsWidget(db_field.verbose_name, db_field.name in self.filter_vertical,
                                                    'permissions')
            field.help_text = ''
        return field


class TabularPermissionsUserAdmin(UserTabularPermissionsAdminBase, UserAdmin):
    pass


class TabularPermissionsGroupAdmin(GroupTabularPermissionsAdminBase, GroupAdmin):
    pass


if app_settings.TABULAR_PERMISSIONS_AUTO_IMPLEMENT:
    try:
        admin.site.unregister(User)
        admin.site.register(User, TabularPermissionsUserAdmin)
        admin.site.unregister(Group)
        admin.site.register(Group, TabularPermissionsGroupAdmin)

    except:
        raise ImproperlyConfigured('Please make sure that django.contrib.auth '
                                   'comes before tabular_permissions in INSTALLED_APPS')
