from __future__ import unicode_literals
from django.utils.translation import ugettext as _


def get_perm_name(model_name, perm_name):
    return '%s_%s' % (perm_name, model_name)


def dummy_permissions_exclude(model):
    """
    A dummy function that excludes nothing,
    :param model:
    :return:
    """
    return False


def custom_permissions_translator(codename, verbose_name, content_type_id):
    """
    A Hook for multi-lingual applications to translate custom permissions
    By default it will try to translated the permission verbose_name

    :param codename: permission codename
    :param verbose_name: permission verbose_name specified on model meta
    :param content_type_id: relevant permission content_type
    :return: a translated verbose_name
    """
    return _(verbose_name)
