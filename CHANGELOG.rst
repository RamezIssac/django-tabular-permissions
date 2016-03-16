* 1.0.9: Minor improve, use django's import_string instead of own hacky code to load the exclude function
* 1.0.8: Fix django version check, add option for dealing with proxy models permissions
* 1.0.7: fixed Issue#2 , 2 models with the same name in different apps + logic enhancement.
* 1.0.5: made TABULAR_PERMISSIONS_EXCLUDE model and app list case insensitive;
  Handle case where excluded model that does not implement the default permissions;
  Fixes around setup.py
* 1.0.3: Fix RTL, move to 'All' instead of 'Select all' , natively translated by django
* 1.0.2: Added 'Select All' for rows.
* 1.0.1: Added tests, travis CI
* 1.0.0: initial concept proof