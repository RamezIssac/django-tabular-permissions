from django.conf import settings
from django.utils.module_loading import import_string

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
user_conf = getattr(settings, 'TABULAR_PERMISSIONS_CONFIG', False)

if user_conf:
    TABULAR_PERMISSIONS_CONFIG.update(user_conf)

AUTO_IMPLEMENT = TABULAR_PERMISSIONS_CONFIG['auto_implement']
TEMPLATE = TABULAR_PERMISSIONS_CONFIG['template']

_base_exclude_apps = ['sessions', 'contenttypes', 'admin']
user_exclude = TABULAR_PERMISSIONS_CONFIG['exclude']
if not user_exclude.get('override', False):
    EXCLUDE_APPS = _base_exclude_apps + user_exclude.get('app', [])
else:
    EXCLUDE_APPS = user_exclude.get('app', [])
EXCLUDE_APPS = [x.lower() for x in EXCLUDE_APPS]

EXCLUDE_MODELS = user_exclude.get('model', [])
EXCLUDE_MODELS = [x.lower() for x in EXCLUDE_MODELS]

model_exclude_func = user_exclude.get('function')
EXCLUDE_FUNCTION = import_string(model_exclude_func)

USE_FOR_CONCRETE = TABULAR_PERMISSIONS_CONFIG['use_for_concrete']
TRANSLATION_FUNC = import_string(TABULAR_PERMISSIONS_CONFIG['custom_permission_translation'])