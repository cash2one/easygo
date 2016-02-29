# -*- coding: utf-8 -*
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TELEVISON(models.Model):
    ''' 剧目（美剧）'''
    title = models.CharField('剧目名称', max_length=64, unique=True)
    title_show = models.CharField('剧目名称-展示用',max_length=128)
    add_time = models.DateTimeField(auto_now_add=True)  # 录入时间点
    introduction = models.TextField('剧目介绍',max_length=1024, default='')
    cover = models.ImageField(upload_to='meiju/%Y/%m%d', null=True)
    cover_origin_url = models.CharField('原始链接', max_length=256, default='')

class EPISODE(models.Model):
    ''' 具体剧集'''
    RES_UNKNOWN = 0
    RES_720P = 720
    RES_1080P = 1080
    RES_CHOICES = {
        (RES_UNKNOWN, '较低清晰度'),
        (RES_720P, '720p'),
        (RES_1080P, '1080p'),

    }

    tvsn = models.ForeignKey('televison')
    subtitle = models.CharField('剧集名称', max_length=128, default='')
    season = models.SmallIntegerField('第几季', default=0)
    resolution = models.SmallIntegerField('清晰度', choices=RES_CHOICES, default=RES_UNKNOWN)
    number = models.SmallIntegerField('第几集')
    zimu = models.CharField('字幕', max_length=64, default='')
    md5str = models.CharField('特征串，防止重复的记录', max_length=32, default='')


    # class Meta:
    #     unique_together = (('tvsn', 'number'),)

class LINK(models.Model):
    ''' 剧集视频源链接'''
    TY_BAIDUYUN = 0
    TY_EMULE = 1
    TY_MAGNET = 2
    TY_BT = 3
    TY_OTHER = 4
    TY_CHOICES = {
        (TY_BAIDUYUN, '百度云'),
        (TY_EMULE, '电驴'),
        (TY_MAGNET, '磁力'),
        (TY_BT, 'bt'),
        (TY_OTHER, '其它'),
    }

    epi = models.ForeignKey('episode', related_name='links')
    typ = models.SmallIntegerField('链接类型', choices=TY_CHOICES, default=TY_BAIDUYUN)
    source = models.CharField('链接', max_length=512)

    class Meta:
        unique_together = (('epi', 'typ', 'source'),)
