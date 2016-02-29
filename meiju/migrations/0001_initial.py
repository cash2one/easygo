# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-01 08:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EPISODE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.SmallIntegerField(default=0, verbose_name='\u7b2c\u51e0\u5b63')),
                ('resolution', models.SmallIntegerField(choices=[(720, '720p'), (0, '\u8f83\u4f4e\u6e05\u6670\u5ea6'), (1080, '1080p')], default=0, verbose_name='\u6e05\u6670\u5ea6')),
                ('number', models.SmallIntegerField(verbose_name='\u7b2c\u51e0\u96c6')),
                ('zimu', models.CharField(default='', max_length=64, verbose_name='\u5b57\u5e55')),
                ('md5str', models.CharField(default='', max_length=32, verbose_name='\u7279\u5f81\u4e32\uff0c\u9632\u6b62\u91cd\u590d\u7684\u8bb0\u5f55')),
            ],
        ),
        migrations.CreateModel(
            name='LINK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.SmallIntegerField(choices=[(3, 'bt'), (0, '\u767e\u5ea6\u4e91'), (1, '\u7535\u9a74'), (4, '\u5176\u5b83'), (2, '\u78c1\u529b')], default=0, verbose_name='\u94fe\u63a5\u7c7b\u578b')),
                ('source', models.CharField(max_length=256, verbose_name='\u94fe\u63a5')),
                ('epi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='meiju.EPISODE')),
            ],
        ),
        migrations.CreateModel(
            name='TELEVISON',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True, verbose_name='\u5267\u76ee\u540d\u79f0')),
                ('title_show', models.CharField(max_length=128, verbose_name='\u5267\u76ee\u540d\u79f0-\u5c55\u793a\u7528')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('introduction', models.TextField(default='', max_length=1024, verbose_name='\u5267\u76ee\u4ecb\u7ecd')),
                ('cover', models.ImageField(null=True, upload_to='meiju/%Y/%m%d')),
                ('cover_origin_url', models.CharField(default='', max_length=256, verbose_name='\u539f\u59cb\u94fe\u63a5')),
            ],
        ),
        migrations.AddField(
            model_name='episode',
            name='tvsn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meiju.TELEVISON'),
        ),
        migrations.AlterUniqueTogether(
            name='link',
            unique_together=set([('epi', 'typ', 'source')]),
        ),
    ]
