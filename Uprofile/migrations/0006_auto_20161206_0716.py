# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 07:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Uprofile', '0005_auto_20161205_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='displayimage',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='displayimage',
            name='image',
            field=models.ImageField(blank=True, height_field='image_height', null=True, upload_to='profile_images/', width_field='image_width'),
        ),
    ]