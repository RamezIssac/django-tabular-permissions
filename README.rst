django-tabular-permissions
##########################
Display Django basic permissions (add, change & delete) in a tabular format that is user friendly, translatable and easy customized.
If you have more customised permissions, the default `FilteredSelectMultiple` widget will also appear to handle those permissions.

*Scroll down for some screen shots.*

Features:
---------
* Permissions are displayed in the active language with app and model ``verbose_name``.
* Any extra custom permissions are displayed in the default admin widget for permissions.
* Customize which apps, models to show in the permissions table. You can also set a exclude function for high-end customization.
* RTL ready, Bootstrap ready.
* Easy customize-able look.
* Tested on Django 1.8 & Django 1.9.
* Tested on Python 2.7, 3.4 & 3.5

.. image:: https://travis-ci.org/RamezIssac/django-tabular-permissions.svg?branch=master
    :target: https://travis-ci.org/RamezIssac/django-tabular-permissions


Installation
------------
You can install `django-tabular-permissions` via Pypi::

    pip install django-tabular-permissions

Usage:
------
Simply add "tabular_permissions" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'tabular_permissions',
    ]

then navigate to User and/or Group change form to see django-tabular-permissions in action.

Settings:
---------

* ``TABULAR_PERMISSIONS_EXCLUDE``

Control which apps, models to show in the permissions table.
By default tabular_permissions exclude contrib apps ``sessions`` , ``contenttypes`` and ``admin`` apps from 
showing their models in the permissions table.
You can add (or override) those apps and/or specify models to exclude, like this::

    TABULAR_PERMISSIONS_EXCLUDE = {
        'app': [],
        'model': [],
        'function': 'tabular_permissions.helpers.TabularPermissionDefaultExcludeFunction', 
                     # A dotted path to a class that implement ``__call__`` that takes model as an argument.
        'override': False # Set to True to override default behavior.
    }    


* ``TABULAR_PERMISSIONS_AUTO_IMPLEMENT``

By default, just by including `tabular_permissions` in your installed_apps, the ``django.contrib.admin.UserAdmin`` (and ``GroupAdmin``) are "patched" to include the tabular_permissions widget.
If you have a custom UserAdmin, then set this option to False and make sure you either:

1. Inherit from `TabularPermissionsUserAdmin` for User admin and from``TabularPermissionsGroupAdmin`` for group admin
2. Inherit from ``UserTabularPermissionsAdminBase`` and ``GroupTabularPermissionsAdminBase`` before admin.ModelAdmin or UserAdmin/GroupAdmin,
3. Set the user_permissions widget to ``tabular_permissions.widgets.TabularPermissionsWidget`` and remember to send a 3rd argument 'permissions' when in Group admin. See ``tabular_permissions.admin`` for information.


* ``TABULAR_PERMISSIONS_TEMPLATE``

Default to 'tabular_permissions/admin/tabular_permissions.html`.
You can either extend or override this template for maximum control.

* ``TABULAR_PERMISSIONS_USE_FOR_CONCRETE``

Default `True`. Till now (Feb 1 2016 - django 1.9), there is an inconsistency with proxy models permissions (ticket `11154 <https://code.djangoproject.com/ticket/11154>`_)
So in case you have proxy models and you create their permissions by hand (via this `gist <https://gist.github.com/magopian/7543724>`_ maybe)
Turn off this option in order to correctly assign your newly created permissions via django-tabular-permissions widget.


JavaScript:
-----------
Located at 'static/tabular_permissions/tabular_permissions.js', it have 3 responsibilities:

1. Upon form submit, the checked permissions in the table are dynamically appended to the form default permission input 
   so the backend can carry on its functionality normally and correctly. 
2. Add handlers for column and row select-all checkboxes.
3. Add a class 'related-widget-wrapper-user-permissions' to the div.related-widget-wrapper
   that contains the table, it serves when you need to manipulate the table container.


Screenshots:
------------
Basic Demo

.. image:: http://i.imgsafe.org/c851707.jpeg
    :target: http://i.imgsafe.org/c851707.jpeg
    :alt: Basic demo

With Custom permission behaviour

.. image:: http://i.imgsafe.org/c506554.jpeg
    :target: http://i.imgsafe.org/c506554.jpeg
    :alt: With Custom permission behaviour

RTL and localized

.. image:: http://i.imgsafe.org/4892b01.jpeg
    :target: http://i.imgsafe.org/4892b01.jpeg
    :alt: RTL and localized

-------

Enjoy and feel free to report any bugs or make pull requests.