# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-05-29 08:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_variationgenotype_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variationgenotype',
            name='box_color',
            field=models.CharField(default='', max_length=50),
        ),
    ]
