# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-16 14:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0016_auto_20170615_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='associationmember',
            name='association',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='associationmembers', to='sales.Association'),
        ),
    ]
