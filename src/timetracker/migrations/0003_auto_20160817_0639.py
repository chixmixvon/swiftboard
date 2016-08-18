# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-17 06:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetracker', '0002_auto_20160816_0350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='user',
        ),
        migrations.RemoveField(
            model_name='project',
            name='company',
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
