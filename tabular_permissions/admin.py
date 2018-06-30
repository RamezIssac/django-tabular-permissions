from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group, GroupAdmin
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from tabular_permissions.widgets import TabularPermissionsWidget
from . import app_settings

User = get_user_model()


class UserTabularPermissionsMixin(object):
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        field = super(UserTabularPermissionsMixin, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'user_permissions':
            field.widget = TabularPermissionsWidget(db_field.verbose_name, db_field.name in self.filter_vertical)
            field.help_text = ''
        return field


class GroupTabularPermissionsMixin(object):
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        field = super(GroupTabularPermissionsMixin, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'permissions':
            field.widget = TabularPermissionsWidget(db_field.verbose_name, db_field.name in self.filter_vertical,
                                                    'permissions')
            field.help_text = ''
        return field


class TabularPermissionsUserAdmin(UserTabularPermissionsMixin, UserAdmin):
    pass


class TabularPermissionsGroupAdmin(GroupTabularPermissionsMixin, GroupAdmin):
    pass


if app_settings.AUTO_IMPLEMENT:
    try:
        admin.site.unregister(User)
        admin.site.register(User, TabularPermissionsUserAdmin)
        admin.site.unregister(Group)
        admin.site.register(Group, TabularPermissionsGroupAdmin)

    except:
        raise ImproperlyConfigured('Please make sure that django.contrib.auth '
                                   'comes before tabular_permissions in INSTALLED_APPS')
