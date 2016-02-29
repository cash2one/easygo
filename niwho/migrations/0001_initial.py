# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-12 17:10
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('openid', models.CharField(max_length=64, verbose_name='id\u5b57\u7b26\u4e32')),
                ('typ', models.SmallIntegerField(choices=[(0, '\u5fae\u4fe1\u7528\u6237')], default=0, verbose_name='\u7528\u6237\u6765\u6e90')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
