----------
CHANGELOG
----------
 v 2.9.1 (7 June 2022)
  - Django 4 Upgrade. (@youssriaboelseod)

 v 2.9 (11 December 2021)
  - Respect model default permission (Case of stalled permission in database due to removed default permissions)

 v 2.8 (15 September 2020)
  - Changed default of use_for_concrete

 v 2.7 (16 August 2020)
  - Assert Django 3.1 Support.
  - Adds Django 3.1 to travis matrix.

 v 2.6 (3 April 2020)
  - Better aim at working with Custom User/Group ModelAdmin out-of-box (Thanks @abahnihi )

 v 2.5 (1 February 2020)
  - Hinted `collectstatic` in installation docs (#14)
  - Fixes possible non unique HTML ID. (#13)

 v 2.4 (19 December 2019)
  - Added `custom_permissions_customization_func` to control the extra permissions not displayed on main permissions table.

 v 2.3 (25 July 2019)
  - Added native javascript event to wait for the full page load to start (Thanks @Filipe-Souza)

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