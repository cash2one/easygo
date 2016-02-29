# -*- coding: utf8 -*-
from __future__ import print_function

from django.conf import settings
import redis

_redis_instances = {}
instance_redis_queries = redis.StrictRedis(**settings.REDIS['default'])

def get(name='default'):
    if _redis_instances.get(name, None):
        return _redis_instances[name]

    _redis_instances[name] = redis.StrictRedis(**settings.REDIS[name])
    return _redis_instances[name]
