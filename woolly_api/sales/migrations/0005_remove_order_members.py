# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-08 08:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_order_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='members',
        ),
    ]
