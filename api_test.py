#!/usr/bin/env python3
import sys
import time
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'monitor.settings'
import django
django.setup()
from zabbix.dbmod import DBMod
from zabbix.zabbix_api import *
from zabbix.contect import *

if __name__ == '__main__':
        z = ZabbixApi()
        # ah = z.getAllGroup()
        dbmode = DBMod()
        a = dbmode.FromGroupidGetHostLoadid('SSP')
        print(a)
        # z.getGroupAvgTraff(grp_name,'out')


        # print(z.getHostTraff(10164,'in'))
        # z.getHistoryTraff(26386)
