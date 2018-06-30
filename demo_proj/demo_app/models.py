# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class ModelWithDefaultPermissions(models.Model):
    name = models.CharField(max_length=100)


class ModelWithEditedDefaultPermission(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        default_permissions = ('change',)


class ModelWithCustomPermissions(models.Model):
    class Meta:
        permissions = (("can_deliver_pizzas", "Can deliver pizzas"),)


class ModelWithCustomPermissionsNoDefault(models.Model):
    class Meta:
        default_permissions = ()
        permissions = (("can_do_stuff", "Can Do stuff"),
                       ("can_do_more_stuff", "Can do more stuff"),
                       )


class ModelWithNoPermissions(models.Model):
    class Meta:
        default_permissions = ()
