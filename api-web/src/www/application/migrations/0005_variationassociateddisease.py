# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-05-23 07:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_variationblockpublicationtext_pubmedid'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariationAssociatedDisease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease_name', models.CharField(default='', max_length=50)),
                ('is_disabled', models.BooleanField(default=False)),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Variation')),
            ],
        ),
    ]
