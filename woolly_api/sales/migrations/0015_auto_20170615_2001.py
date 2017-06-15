# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 20:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0014_auto_20170615_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemspecifications',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemspecifications', to='sales.Item'),
        ),
        migrations.AlterField(
            model_name='itemspecifications',
            name='woolly_user_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemspecifications', to='authentication.WoollyUserType'),
        ),
    ]
