#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

from socialnetwork import __version__


setup(
    name='django-socialnetwork',
    version=__version__,
    description=('Provides functionality to login and share with social '
        'networks to Django.'),
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')
    ).read(),
    author=u'Gabriel González',
    author_email='zurg.cei@gmail.com',
    url='https://github.com/gGonz/django-socialnetwork',
    license='Apache License (2.0)',
    install_requires=[
        'Django >= 1.4',
        'requests',
        'requests_oauthlib',
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
	'License :: OSI Approved :: Apache Software License',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
	'Topic :: Software Development :: Libraries :: Python Modules',
	'Topic :: Internet',

    ]
)

