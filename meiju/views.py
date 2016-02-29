#encoding=utf8

import json

from django.shortcuts import render
from django.http import HttpResponse

import meiju.controllers as m_ctrl

# Create your views here.
def get_televison(request):
    sinceid = int(request.GET.get('sinceid', 0))
    num = int(request.GET.get('num', 20))
    ret = m_ctrl.get_meiju(sinceid, num)
    return HttpResponse(json.dumps(ret), content_type="application/json")

def get_episode(request):
    tvid = int(request.GET.get('tvid', 1))
    ret = m_ctrl.get_episode(tvid)
    return HttpResponse(json.dumps(ret), content_type="application/json")

def get_episode_seasons(request):

    tvid = int(request.GET.get('tvid', 1))
    ret = m_ctrl.get_episode_seasons(tvid)
    return HttpResponse(json.dumps(ret), content_type="application/json")

def get_episode_spec(request):
    tvid = int(request.GET.get('tvid', 1))
    season = int(request.GET.get('season', 1))
    sinceid = int(request.GET.get('sinceid', 0))
    num = int(request.GET.get('num', 20))
    ret = m_ctrl.get_episode_spec(tvid, season, sinceid, num)
    return HttpResponse(json.dumps(ret), content_type="application/json")
