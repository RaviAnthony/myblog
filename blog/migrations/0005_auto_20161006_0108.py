# -*- coding: utf-8 -*-
# Generated by Django 1.10b1 on 2016-10-05 19:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blog_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='blog',
            name='publish',
            field=models.DateField(default=datetime.datetime(2016, 10, 5, 19, 38, 51, 109000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
