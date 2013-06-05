#!/usr/bin/python
# -*- coding: utf-8 -*-
from distutils.core import setup


setup(
    name='django-socialnetwork',
    version='0.0.1',
    author=u'Gabriel González',
    author_email='zurg.cei@gmail.com',
    description=('Django app that provides login and share access with '
        'social networks.'),
    long_description=open('README.txt').read(),
    license='LICENSE',
    url='https://github.com/gGonz/django-socialnetwork',
    packages=['socialnetwork'],
    install_requieres=[
        'Django >= 1.4',
        'requests',
        'requests_oauhtlib',
    ],
)

