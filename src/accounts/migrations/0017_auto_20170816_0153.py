# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 01:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20170816_0131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='walletprofile',
            name='id',
        ),
        migrations.AlterField(
            model_name='walletprofile',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='wallet', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
