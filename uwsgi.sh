#!/bin/sh
web_dir=`pwd`
port=9001
kill -9 `ps aux|grep uwsgi|grep ${port}|grep -v grep|awk '{print $2}'`
uwsgi --socket 127.0.0.1:${port} --chdir $web_dir --wsgi-file ${web_dir}/monitor/wsgi.py -d uwsgi.log