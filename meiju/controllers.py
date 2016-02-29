# -*- coding: utf8 -*-
from __future__ import print_function
# import io
import hashlib
import logging
import json

import io
from .models import TELEVISON, EPISODE, LINK
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File

logger = logging.getLogger('meiju')

def test_televsion(task):
    for k,v in task.iteritems():
        chname, ename = k.split(' ', 1)
        TELEVISON.objects.create(title=chname, title_show=k,)

def new_televison(cover_data, cover_name, indro, name, name_show, cover_url):
    try:
        # from django.core.files.uploadedfile import SimpleUploadedFile
        fu = None
        if cover_data:
            fu = File(io.BytesIO(cover_data))
        tel = TELEVISON.objects.create(title=name, title_show=name_show,
            introduction=indro, cover_origin_url=cover_url
          )
    except Exception, e:  # 这里是并发创建同一条记录的情况
        raise e
    if fu:
        tel.cover.save(cover_name, fu)
        fu.close()
    return tel

def exist_televison(name):
    tel = TELEVISON.objects.filter(title=name).first()
    return tel

def episode(telid, season, number, resol, zimu, subtitle):
    season = int(season) if season else 0
    number = int(number) if number else 0
    resol = int(resol) if resol else 0
    zimu = zimu if zimu else ''

    md5str = '%d%d%d%d%s%s' %(telid, season, number, resol, zimu, subtitle)
    md5str = hashlib.md5(md5str.encode('utf8')).hexdigest()
    epi = EPISODE.objects.filter(md5str=md5str).first()
    if epi:
        return epi.id
    else:
        epi = EPISODE.objects.create(tvsn_id=telid, season=season, number=number,
                resolution=resol, zimu=zimu, md5str=md5str, subtitle=subtitle)
        return epi.id

def link(epiid, href):
    try:
       if 'baidu' in href:
           typ = LINK.TY_BAIDUYUN
       elif 'ed2k' in href:
           typ = LINK.TY_EMULE
       elif 'magnet' in href:
           typ = LINK.TY_MAGNET
       elif 'torrent' in href:
           typ = LINK.TY_BT
       else:
           typ = LINK.TY_OTHER
       if not LINK.objects.filter(epi_id=epiid, typ=typ, source=href).exists():
           LINK.objects.create(epi_id=epiid, typ=typ, source=href)
           logger.info('new:%d,%d,%s'%(epiid, typ, href))
    except Exception,e:
        logger.error(str(e))

def get_meiju(sinceid=0, num=20):
    '''
        {
            id1:{
            'title': 剧目,
            'indro': 介绍,
            'cover': 封面,
            "content":{ # 请求更新的，不是一次传过去
                season1:{
                    number1:{
                        links:[]
                    }
                }
            }
            }


        }
    '''
    tels = TELEVISON.objects.filter(id__gt=sinceid)[:num]
    ret_list = []
    for tel in tels:
        ret_list.append({
                'id': tel.id,
                'title': tel.title,
                'indro': tel.introduction,
                'cover': tel.cover_origin_url,  # tel.cover.url
                'contents': {},
                'seasons': get_episode_seasons(tel.id),
                'status': {'scrollinfo': {}, 'ot':{}}, # 前端状态存储
            })
    lastid = tels[tels.count()-1].id if tels else sinceid
    more = (tels.count() == num) and (lastid > sinceid)
    return {'data': ret_list, 'sinceid': lastid, 'more': more}

def get_episode(tvid):
    '''
    SODE.objects.filter(tvsn_id=5).values_list('season',flat=True).distinct().order_by('season')url(r'^get_episode/?', views.get_episode),
    {
        'season1':[{
            'number1': 1,
            'links': [xx,],
            'res': 720,
        },{...}]
    }
    '''
    eps = EPISODE.objects.filter(tvsn_id=tvid).order_by('season', 'number')
    ret = {}
    ret_list = []
    for ep in eps:
        if ep.season not in ret:
            ret[ep.season] = []
        ret[ep.season].append({'number':ep.number,'res': ep.resolution, 'subtitle': ep.subtitle,'links': [lk.source for lk in ep.links.all()]})
    for k, v in ret.iteritems():
        ret_list.append({'season':k, 'episode':ret[k]})

    ret_list.sort(key=lambda x:x['season'], reverse=True)
    return ret_list

def get_episode_seasons(tvid):

    seasons = EPISODE.objects.filter(tvsn_id=tvid).values_list('season',flat=True).distinct().order_by('-season')
    sea = []
    for s in seasons:
        sea.append(s)
    return sea
def get_episode_spec(tvid, season, sinceid=0, num=20):
    '''
    {
        'season1':[{
            'number1': 1,
            'links': [xx,],
            'res': 720,
        },{...}]
    }
    '''
    eps = EPISODE.objects.filter(tvsn_id=tvid, season=season).order_by('number', 'id').filter(id__gt=sinceid)[:num]
    ret = {}
    ret_list = []
    for ep in eps:
        if ep.season not in ret:
            ret[ep.season] = []
        ret[ep.season].append({'number':ep.number,'res': ep.resolution, 'subtitle': ep.subtitle,'links': [lk.source for lk in ep.links.all()]})
    for k, v in ret.iteritems():
        ret_list.append({'season':k, 'episode':ret[k]})

    # ret_list.sort(key=lambda x:x['season'], reverse=True)
    lastid = eps[eps.count()-1].id if eps else sinceid
    more = (eps.count() == num) and (lastid > sinceid)
    return {'data': ret_list[0] if ret_list else {}, 'status': {'sinceid': lastid, 'more': more, 'y': 0, 'currentid': -1}}

def fix_epi():
    import re
    pattern = re.compile('S(\d+)E(\d+)(?:\s+(\d+)p)?(?:\s+([\w-]+))?', re.U)
    for epi in EPISODE.objects.all():
        mat = pattern.search(epi.subtitle)
        print (epi.id)
        if mat:
            epi.season = int(mat.group(1)) if mat.group(1) else 0
            epi.number = int(mat.group(2)) if mat.group(2) else 0
            epi.resolution = int(mat.group(3)) if mat.group(3) else 0
            epi.zimu = mat.group(4) if mat.group(4) else ''

            md5str = '%d%d%d%d%s%s' %(epi.tvsn_id, epi.season, epi.number, epi.resolution, epi.zimu, epi.subtitle)
            md5str = hashlib.md5(md5str.encode('utf8')).hexdigest()
            epi.md5str = md5str
            epi.save()

