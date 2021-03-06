# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 11:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('active', models.BooleanField(db_index=True)),
                ('level', models.IntegerField(db_index=True, default=0, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryHierarchy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_category', to='menu.Category')),
                ('parent_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_category', to='menu.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('active', models.BooleanField(db_index=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('name', 'price')]),
        ),
        migrations.AddField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(blank=True, to='menu.Product'),
        ),
        migrations.AddField(
            model_name='category',
            name='sub_categories',
            field=models.ManyToManyField(blank=True, related_name='parent_categories', through='menu.CategoryHierarchy', to='menu.Category'),
        ),
    ]
