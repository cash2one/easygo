# -*- coding: utf8 -*-
from __future__ import print_function

import gevent
import gevent.monkey
gevent.monkey.patch_all()
from django.core.management.base import BaseCommand
from .utils import MyWorker

class Command(BaseCommand):
    help = '获取美剧信息'

    def handle(self, *args, **options):
        MyWorker().do_jobs()


if __name__ == '__main__':
    pass
