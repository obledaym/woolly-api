# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 07:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='woollyuser',
            name='type',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='authentication.WoollyUserType'),
        ),
    ]
