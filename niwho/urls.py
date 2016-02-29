# -*- coding: utf8 -*-
from __future__ import print_function

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^verify/?$', views.temp_verify),
    url(r'^wx/?$', views.temp_verify),
    url(r'^info/?$', views.info),
]
