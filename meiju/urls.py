# -*- coding: utf8 -*-
from __future__ import print_function

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^get_televison/?', views.get_televison),
    url(r'^get_episode_spec/?', views.get_episode_spec),
    url(r'^get_episode/?', views.get_episode),
    url(r'^get_episode_seasons/?', views.get_episode_seasons),
]
