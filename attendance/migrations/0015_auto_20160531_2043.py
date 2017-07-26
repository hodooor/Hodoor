# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0014_swipe_corrected_swipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='swipe',
            old_name='corrected_swipe',
            new_name='correct_swipe',
        ),
        migrations.AddField(
            model_name='swipe',
            name='correcting',
            field=models.BooleanField(default=False),
        ),
    ]
