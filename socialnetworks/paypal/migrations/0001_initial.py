# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PayPalOAuthProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_uid', models.CharField(max_length=255, unique=True, null=True, verbose_name='uid', blank=True)),
                ('oauth_access_token', models.CharField(max_length=255, null=True, verbose_name='OAuth access token', blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date', null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, auto_now_add=True, null=True, verbose_name='last modified')),
                ('oauth_access_token_expires_at', models.DateTimeField(null=True, verbose_name='OAuth access token expires at', blank=True)),
                ('oauth_refresh_token', models.CharField(max_length=255, null=True, verbose_name='OAuth refresh token', blank=True)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'paypal profile',
                'verbose_name_plural': 'paypal profiles',
            },
            bases=(models.Model,),
        ),
    ]
