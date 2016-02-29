# -*- coding: utf8 -*-
from __future__ import print_function

import gevent
import gevent.monkey
gevent.monkey.patch_all()
from bs4 import BeautifulSoup
import requests
import re
import logging

from gevent.queue import Queue
from gevent.pool import Pool
from gevent.threadpool import ThreadPool

import meiju.controllers as m_ctrl

logger = logging.getLogger('meiju')

class MyCrawler(object):
    def __init__(self):
        self.pool = Pool(10)
        self.tasks = Queue()

    def init_tasks(self):
        resp = requests.get('http://www.ttmeiju.com/summary.html')
        assert resp.status_code==200
        soup = BeautifulSoup(resp.text)
        tb = soup.find('table')

        def mya(tag):
            return tag.name=='a' and tag.parent.name=='td'

        meiju={}
        for atag in tb.find_all(mya)[3:]:
            meiju[atag.string] = atag['href']
            self.tasks.put_nowait({'key':atag.string, 'val': atag['href']})

        print (meiju)

    def do_jobs(self):
        self.init_tasks()

        while not self.tasks.empty():
            task = self.tasks.get()
            self.before(task)
            self.pool.spawn(self.work, task).rawlink(self.after)
            # 等待任务完成
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        self.pool.join()

    def work(self, task):
        print ('子类实现')

    def before(self, task):
        print('')

    def after(self, asynret):
        print('')

class MyWorker(MyCrawler):
    def __init__(self):
        super(MyWorker, self).__init__()
        self.workerpools = {}
        self.pattern = re.compile('(\w+)\s+(.+)S(\d+)E(\d+)(?:\s+(\d+)p(?:(.+))?)?',re.U)
        self.pattern = re.compile('(\w+)\s+(.+)(?:\s+S(\d+)E(\d+))?(?:\s+(\d+)p(?:(.+))?)?',re.U)
        self.pattern = re.compile('S(\d+)E(\d+)(?:\s+(\d+)p)?(?:\s+([\w-]+))?', re.U)
    def before(self, task):
        pass

    def after(self, ret):
        pass

    def work(self, task, more=True):
        print ('yes,i do', task)
        # 获取分页信息
        resp = requests.get(task['val'])
        soup = BeautifulSoup(resp.text)
        self.parse(task, soup)


        if not more:
            return
        pg = soup.find('div', class_='pages')
        if not pg:
            return

        current_page = int(pg.div.strong.string)
        asx = pg.find_all('a')
        if asx[-1].has_attr('class'):
            # 有下一页，则当前末页需要more处理
            more = True
            last_page = int(asx[-2].string)
        else:
            more = False
            last_page = int(asx[-1].string)
        __ = []
        # 这里并发网络访问
        for x in range(current_page+1, last_page+1):
            __.append(gevent.spawn(self.work, {'key': task['key'],
                'val': '%s?page=%d' % (task['val'].rsplit('?', 1)[0], x)}, more and x==last_page))
        gevent.joinall(__)
            # self.pool.spawn(self.work, {'key': task['key'],'val':'%s?page=%d' % (task['val'].rsplit('?', 1)[0], x)}, more and x==last_page)

    def parse(self, task, soup):
        print ('parse: ',task)
        name = task['key'].split(' ',1)[0]
        tel = m_ctrl.exist_televison(name)

        if not tel:
            # 简介
            indro = soup.find('div', class_='newstxt')
            indro_text = ''
            if indro:
                for string in indro.stripped_strings:
                    indro_text += string

            # 封面图片
            cover_url = ''
            try:
                cover_url =  soup.find('div',class_='seedpic').img['src']
                resp = requests.get(cover_url)
            except Exception, e:
                logger.error(e)
                resp = type('_innerclass_', (object,),{'content':None})
            tel = m_ctrl.new_televison(resp.content,
                    cover_url.rsplit('/', 1)[-1],
                    indro_text,
                    name,
                    task['key'],
                    cover_url
                    )
        # seed
        try:
            seedtable = soup.find_all('table', class_='seedtable')[-1]
        except Exception,e:
            logger.error(e)
            return

        tr = soup.find_all('tr', class_='Scontent')
        for ttr in tr:
            tds = ttr.find_all('td')

            mat = self.pattern.search(tds[1].string)
            if mat:
               zimu = mat.group(4)
               epiid = m_ctrl.episode(tel.id, mat.group(1), mat.group(2), mat.group(3), zimu, tds[1].string)
               for lk in tds[2].find_all('a'):
                   #logger.info('@%d,%s' %(epiid,tds[1].string.strip()))
                   href = lk['href']
                   m_ctrl.link(epiid, href)
            else:
               epiid = m_ctrl.episode(tel.id, None, None, None, None, tds[1].string)
               for lk in tds[2].find_all('a'):
                   logger.info('@%d,%s' %(epiid,tds[1].string.strip()))
                   href = lk['href']
                   m_ctrl.link(epiid, href)

if __name__ == '__main__':
    worker = MyWorker()
    import pdb;pdb.set_trace()
    worker.do_jobs()
