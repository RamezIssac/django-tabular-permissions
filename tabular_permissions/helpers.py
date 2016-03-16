from __future__ import unicode_literals


def get_perm_name(model_name, perm_name):
    return '%s_%s' % (perm_name, model_name)


class TabularPermissionDefaultExcludeFunction(object):
    def __call__(self, model):
        return False


