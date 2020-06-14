# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-05-29 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_auto_20170529_0808'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariationEffectNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('popcode', models.TextField(default='')),
                ('genotype', models.TextField(default='')),
                ('risk', models.TextField(default='')),
                ('odd_ratio', models.TextField(default='')),
                ('evidences', models.TextField(default='')),
                ('pmid', models.TextField(default='')),
            ],
        ),
    ]
