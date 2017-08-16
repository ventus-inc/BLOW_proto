# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 05:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '__first__'),
        ('accounts', '0004_auto_20170808_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='wallet_id',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='wallet',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to='wallets.WalletProfile'),
        ),
    ]
