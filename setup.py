import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-tabular-permissions',
    version='1.0.0',
    packages=['tabular_permissions'],
    include_package_data=True,
    license='BSD License',
    description='Display django permissions in a tabular format that is user friendly, and highly customisable',
    long_description=README,
    url='https://radev.io/',
    author='Ramez Ashraf',
    author_email='ramez@radev.io',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)