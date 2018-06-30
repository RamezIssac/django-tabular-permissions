django-tabular-permissions
##########################
Display model permissions in a tabular widget that is user friendly, translatable and customizeable.


Features:
---------
* Permissions and their relevant app and models names are displayed in the active language.
* Permisions are displayed in a table that contain the default model permissions **plus** any custom permissions.
* Customize which apps, models to show in the permissions table. You can also set a exclude function for high-end customization.
* RTL ready, Bootstrap ready.
* Easy customize-able look.
* Django >= 1.11
* Tested on Python 2.7, 3.5, 3.6 & 3.7
* Default `FilteredSelectMultiple` widget will appear only if you have custom permissions that are not model related (ie directly created by code or hand)



.. image:: https://travis-ci.org/RamezIssac/django-tabular-permissions.svg?branch=master
    :target: https://travis-ci.org/RamezIssac/django-tabular-permissions


Installation
------------
You can install `django-tabular-permissions` via Pypi::

    pip install django-tabular-permissions


and add "tabular_permissions" to your INSTALLED_APPS setting (at any place after `django.contrib.auth`) ::

    INSTALLED_APPS = [
        'django.contrib.auth',
         ....
        'tabular_permissions',
    ]

then navigate to User and/or Group change form to see `tabular_permissions` in action.

Configuration:
--------------
Tabular_permissions possible configurations and their default::

    TABULAR_PERMISSIONS_CONFIG = {
        'template': 'tabular_permissions/admin/tabular_permissions.html',
        'exclude': {
            'override': False,
            'app': [],
            'model': [],
            'function':'tabular_permissions.helpers.dummy_permissions_exclude'
        },
        'auto_implement': True,
        'use_for_concrete': True,
        'custom_permission_translation': 'tabular_permissions.helpers.custom_permissions_translator',
    }


`template`
  the template which contains the permissions table, you can always customize this default by extending or overriding

`exclude`
  Control which apps, models to show in the permissions table.

  By default ``tabular_permissions`` exclude `sessions` , `contenttypes` and `admin` apps from showing their models in the permissions table. If you want to show them you can switch ``override`` to `False`.

  ``app`` & ``model`` lists would contain the names of the apps and models you wish to exclude.

  ``function`` is a dotted path of a custom function which receive the model as a parameter to decide either to exclude it or not, default to a dummy function that always return False (ie do not exclude)

auto_implement
  By default, just by including `tabular_permissions` in your installed_apps, the ``django.contrib.admin.UserAdmin`` (and ``GroupAdmin``) are "patched" to include the tabular_permissions widget.
  If you have a custom UserAdmin, then set this option to False and make sure you either:

  1. Inherit from `TabularPermissionsUserAdmin` for User admin and from``TabularPermissionsGroupAdmin`` for group admin
  2. Inherit from ``UserTabularPermissionsAdminBase`` and ``GroupTabularPermissionsAdminBase`` before admin.ModelAdmin for UserAdmin/GroupAdmin,
  3. Set the user_permissions widget to ``tabular_permissions.widgets.TabularPermissionsWidget`` and remember to send a 3rd argument 'permissions' when in Group admin. See ``tabular_permissions.admin`` for information.

use_for_concrete
  There is an inconsistency with proxy models permissions (ticket `11154 <https://code.djangoproject.com/ticket/11154>`_).

  So in case you have proxy models and you create their permissions by hand (via this `gist <https://gist.github.com/magopian/7543724>`_ maybe), then turn off this option in order to correctly assign your newly created permissions in django-tabular-permissions widget.

custom_permission_translation
  a dotted path function to translate the custom permission.
  This function gets passed the permissions `codename`, `verbose_name` and its relevant `content_type_id`.
  The function will try to translate the permission verbose_name.

JavaScript:
-----------
Located at 'static/tabular_permissions/tabular_permissions.js', it have 2 responsibilities:

1. Upon form submit, the checked permissions in the table are dynamically appended to the form default permission input so the backend can carry on its functionality normally and correctly.
2. Add handlers for column and row `select-all` checkboxes.


Compatibility:
--------------
Current version 2.0 supports only django >= 1.11
For earlier versions of django use django-tabular-permissions 1.0.9.




Screenshots:
------------
Basic Demo

.. image:: https://rasystems.io/static/images/tabular_permissions/tp_1.png
    :target: https://rasystems.io/static/images/tabular_permissions/tp_1.png
    :alt: Basic demo

RTL and localized

.. image:: https://rasystems.io/static/images/tabular_permissions/tp_ar.png
    :target: https://rasystems.io/static/images/tabular_permissions/tp_ar.png
    :alt: RTL and localized

With Custom permission behaviour

.. image:: https://rasystems.io/static/images/tabular_permissions/tp_extra.png
    :target: https://rasystems.io/static/images/tabular_permissions/tp_extra.png
    :alt: With Custom permission

-------

Enjoy and feel free to report any bugs or make pull requests.cutom permissio