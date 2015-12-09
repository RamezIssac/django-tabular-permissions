from django.conf import settings

TABULAR_PERMISSIONS_TEMPLATE = getattr(settings, 'TABULAR_PERMISSIONS_TEMPLATE',
                                       'tabular_permissions/admin/tabular_permissions.html')
_base_exclude_app = ['sessions', 'contenttypes', 'admin']
user_exclude = getattr(settings, 'TABULAR_PERMISSIONS_EXCLUDE', {'override': False, 'app': [], 'model': []})
if not user_exclude.get('override', False):
    TABULAR_PERMISSIONS_EXCLUDE_APPS = _base_exclude_app + user_exclude.get('app', [])
else:
    TABULAR_PERMISSIONS_EXCLUDE_APPS = user_exclude.get('app', [])

TABULAR_PERMISSIONS_EXCLUDE_MODELS = user_exclude.get('model', [])
