# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 13:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Feedbacks', '0008_auto_20170129_1025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indicado',
            old_name='Cliente',
            new_name='cliente',
        ),
    ]
