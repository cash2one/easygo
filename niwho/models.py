#coding=utf8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class OpenUser(User):
    TYP_WX = 0
    TYP_CHOICE = (
        (TYP_WX, u'微信用户'),
    )
    openid = models.CharField(u'id字符串', max_length=64)
    typ = models.SmallIntegerField(u'用户来源', choices=TYP_CHOICE, default=TYP_WX)
