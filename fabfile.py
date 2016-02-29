# -*- coding: utf8 -*-
from __future__ import absolute_import, print_function

import os

from fabric.api import *  # NOQA

def help():
    print('fab cmd -H host -u user --set ENV=$env')


WORKDIR = env.get('WORKDIR', '/webapps/niwhox/easygo')

if env.hosts:  # with remote hosts
    do = sudo
else:
    do = local

def _wrap(fn):
    def wrapped(*args, **kwargs):
        with cd(WORKDIR):
            fn(*args, **kwargs)
    return wrapped

#managing django app

@_wrap
def app_stop():
    with settings(warn_only=True):
        do('test -f var/gunicorn.pid && kill `cat var/gunicorn.pid`')

@_wrap
def app_start():
    do('gunicorn --config easygo/gunicorn.config easygo.wsgi')

@_wrap
def app_restart():
    app_stop()
    app_start()

@_wrap
def celery_start():
    do('celery multi start worker1 -A easygo --pidfile=var/celery.pid --logfile=var/celery.log')

@_wrap
def celery_stats():
    do('celery -A easygo inspect stats')

@_wrap
def celery_working_tasks():
    do('celery -A easygo inspect active')

@_wrap
def celery_stop():
    do('celery multi stopwait worker1 --pidfile=var/celery.pid')

@_wrap
def celery_restart():
    do('celery multi restart worker1 -A easygo --pidfile=var/celery.pid --logfile=var/celery.log')

@_wrap
def pip_install():
    do('pip install -r pip_requirements.txt')

def deploy_frontend():
    do('cd easygo/static/public && bower install --allow-root')
    cache_staticfiles()
    do('python manage.py collectstatic')

def supervisor_restart():
        pass

@_wrap
def cache_staticfiles():
    do('cp -r easygo/static/public/bower_components/bootstrap/dist/fonts easygo/static/public/bower_components/flat-ui/dist/css/')
    do('rm -rf easygo/static/public/bower_components/Jcrop/demos/')
    do('sed -i "s/@import//ig" easygo/static/public/bower_components/Buttons/css/buttons.css')
    do('sed -i "s/@import//ig" easygo/static/public/bower_components/Buttons/showcase/css/buttons.css')

def grunt():
    with cd(os.path.join(WORKDIR, 'easygo/static/easygo')):
        do('npm install')
        do('grunt')

@_wrap
def deploy():
    do('git reset --hard HEAD')
    do('git pull origin master')
    do('echo $(date "+%Y%m%d %H:%M:%S") $(git rev-parse HEAD) ' + whoami() + ' >> var/release.log')
    # pip_install()
    try:
        # grunt()
        deploy_frontend()
        celery_restart()
        app_restart()
        supervisor_restart()
        do('echo "... ok" >> var/release.log')
    except:
        do('echo "... ERROR" >> var/release.log')
        raise

def whoami():
    import getpass
    return getpass.getuser()

