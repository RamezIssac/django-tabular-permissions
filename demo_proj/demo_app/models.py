# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _


class ModelWithDefaultPermissions(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('Model with all default permissions')


class ModelWithEditedDefaultPermission(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('Model with `change` permissions Only')


class ModelWithCustomPermissions(models.Model):
    class Meta:
        verbose_name = _('Model with default & custom permission')
        permissions = (("can_deliver_pizzas", "Can deliver pizzas"),)


class ModelWithCustomPermissionsNoDefault(models.Model):
    class Meta:
        verbose_name = _('Model with no default permissions & 2 custom permissions')
        default_permissions = ()
        permissions = (("can_do_stuff", "Can do stuff"),
                       ("can_do_more_stuff", "Can do more stuff"),
                       )


class ModelWithNoPermissions(models.Model):
    class Meta:
        default_permissions = ()


class ModelWithChangedDefaultPermissions(models.Model):
    class Meta:
        default_permissions = ('view',)
