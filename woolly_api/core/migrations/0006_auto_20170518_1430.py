# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 14:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20170514_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='woollyusertype',
            name='name',
            field=models.IntegerField(choices=[(1, 'cotisant'), (2, 'non-cotisant'), (3, 'exterieur'), (4, 'tremplin')], max_length=50),
        ),
    ]
