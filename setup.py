#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

METADATA = dict(
    name='django-socialnetwork',
    version='0.0.1',
    author=u'Gabriel González',
    author_email='zurg.cei@gmail.com',
    description=('Django app that provides login and share access with '
        'social networks.'),
    long_description=open('README.txt').read(),
    license='LICENSE',
    url='https://github.com/gGonz/django-socialnetwork',
    install_requires=[
        'Django >= 1.4',
        'requests',
        'requests_oauthlib',
    ],
    include_package_data=True,
    packages=find_packages(),
)


if __name__ == '__main__':
    setup(**METADATA)


