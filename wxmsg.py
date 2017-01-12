#!/usr/bin/env python3
import sys
import time
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'monitor.settings'
import django
django.setup()
from zabbix.dbmod import DBMod
# from zabbix.wxalert import *

if __name__ == '__main__':
	# if len(sys.argv) == 3:
	# 	toparty,content = sys.argv[1:]
	# 	content = time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime()) + content
	# 	toparty = int(toparty)
	# else:
	# 	print('error segments, now exit')
	# 	sys.exit()
	# wechat = WXAlert(toparty,content)
	# wechat.sendMsg()
	d = DBMod()
	print(d.FromEventidGetItemid(489377))