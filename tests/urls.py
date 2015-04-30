# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url


urlpatterns = patterns(
    '',
    url(r'^social/',
        include('socialnetworks.urls', namespace='socialnetworks')),
)
