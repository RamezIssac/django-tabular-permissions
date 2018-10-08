----------
CHANGELOG
----------
 v 2.2 (8 October 2018)
  - Adds view permission supporting Django 2.1

 v 2.1 (16 July 2018)
  - Adds `apps_customization_func` option to allow a full apps customization control. (Thanks to KuwaitNet)

 v 2.0.2 (July 1 2018)
  - Include locale in manifest
  - fix a problem with exclude settings & use plural instead of singular in exclude apps and models settings,
  - Fix RTL checkbox alignment issue


 v 2.0 (June 30 2018)

  - Major breaking release.
  - Added logic to support model custom permissions in an extra column instead of the original widget.
  - Original widget appear only to totally custom permissions created by code.
  - Added demo_project and renewed screen shots


 1.1.1 (Nov 21 2017)

 - Added `model-` prefix for model name css class to prevent conflict *(ie model_name called table)*

 1.1 (Sep 9 2017)

  - Added support for Django 1.11

 1.0.9 (Mar 11 2016)
  - Minor improvement
  - use Django's `import_string` instead of own hacky function to load the exclude function



 1.0.8 (Feb 1 2016)

  - Added option for dealing with proxy models permissions,
  - Fixes Django version check,

 1.0.7 (Dec 24 2015)
  - Fixed Issue#2.
  - Logic enhancement.


* 1.0.4 (Dec 14 2015)

  made TABULAR_PERMISSIONS_EXCLUDE model and app list case insensitive;
  Handle case where excluded model that does not implement the default permissions;
  Fixes around setup.py

 1.0.3
  Fix RTL, move to 'All' instead of 'Select all' , natively translated by django

 1.0.2
  Added 'Select All' for rows.

 1.0.1
  Added tests, travis CI

 1.0.0 (Dec 9 2015)
  initial concept proof