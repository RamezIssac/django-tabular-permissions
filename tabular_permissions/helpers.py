from __future__ import unicode_literals


def get_perm_name(model_name, perm_name):
    return '%s_%s' % (perm_name, model_name)


class TabularPermissionDefaultExcludeFunction(object):
    def __call__(self, model):
        return False


def get_class(path):
    names = path.split('.')
    my_class = names.pop(-1)
    path_adjusted = '.'.join(names)

    mod = __import__(path_adjusted, fromlist=[my_class])
    klass = getattr(mod, my_class)
    return klass
