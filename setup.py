#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

from socialnetworks import __author__, __version__


setup(
    name='django-socialnetworks',
    version=__version__,
    description=('Extends Django with “log in” and “share” functionalities '
                 'for the most common social networks.'),
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')
    ).read(),
    author=__author__,
    author_email='zurg.cei@gmail.com',
    url='https://github.com/gGonz/django-socialnetworks',
    license='Apache License (2.0)',
    install_requires=[
        'Django>=1.5',
        'requests_oauthlib',
        'unidecode',
        'pytz'
    ],
    extras_require={
        'security': 'requests[security]'
    },
    packages=find_packages(),
    include_package_data=True,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet'
    ]
)
