# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Feedbacks', '0004_auto_20170119_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicado',
            name='categoria',
        ),
        migrations.AddField(
            model_name='indicado',
            name='Categ',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='indicado',
            name='Cliente',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Feedbacks.Cliente'),
            preserve_default=False,
        ),
    ]