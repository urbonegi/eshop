# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='active',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(),
        ),
    ]
