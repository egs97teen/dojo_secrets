# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 22:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secrets_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Secret',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('likes', models.ManyToManyField(related_name='likes', to='secrets_app.User')),
                ('secret_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secrets', to='secrets_app.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='comment_user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='likes',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
