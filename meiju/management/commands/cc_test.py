# -*- coding: utf8 -*-
from __future__ import print_function

import gevent
import gevent.monkey
gevent.monkey.patch_all()
gevent.monkey.patch_all(thread=False)

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = '获取美剧信息'

    def handle(self, *args, **options):
        import pdb;pdb.set_trace()
        print('hello')
