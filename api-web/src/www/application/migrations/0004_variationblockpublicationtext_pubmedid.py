# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-05-23 02:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_auto_20170519_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='variationblockpublicationtext',
            name='pubmedid',
            field=models.CharField(default='', max_length=50),
        ),
    ]
