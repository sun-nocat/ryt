# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-09 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yrt', '0003_ticket_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='operaId',
            field=models.CharField(default='None', max_length=10),
        ),
    ]
