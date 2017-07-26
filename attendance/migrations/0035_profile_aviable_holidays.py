# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-06-26 11:51
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0034_auto_20170626_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='aviable_holidays',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.5)]),
        ),
    ]
