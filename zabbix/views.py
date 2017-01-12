from django.shortcuts import render,HttpResponse
import requests
import time
import re
from .base import Base
from .dbmod import DBMod


# Create your views here.


def test(request):
	return HttpResponse('ok')

def AlertInfo(request,event_id,time_stm):
	'''
	通过itemid 返回报警详细页
	:param event_id: 事件ID
	:param time_stm: 时间戳
	:param request:
	:return:
	'''
	zconn = DBMod()
	item_id = zconn.FromEventidGetItemid(event_id)

	#当前报警信息
	current_info = CurrentAlert(item_id,event_id,zconn)

	#历史报警信息
	history_info = HistoryAlert(item_id,zconn)

	#主机触发器列表
	hosttrigger_info = HostTrigger(item_id,zconn)

	return render(request,'zabbix/alert_info.html',{'current_info':current_info,'history_info':history_info,'hosttrigger_info':hosttrigger_info})

def CurrentAlert(item_id,event_id,zconn,time_stm=None):
	current_info = {}
	alert_info = {}
	print(time_stm)
	if time_stm:
		alert_detail = zconn.GetAlertMsg(eventid=event_id)
	else:
		alert_detail = zconn.GetAlertMsg(itemid=item_id)
	if not alert_detail:
		current_info['status'] = 0
		return current_info
	else:
		current_info['status'] =1
	alert_info['user'] = [x[0] for x in alert_detail]
	alert_info['msg'] = alert_detail[0][1].replace('\r','').replace('\\r\\n','\n').replace('：',':').split('\n')
	msg = []
	msg.append(['报警时间',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(alert_detail[0][2]))])
	for each_msg in alert_info['msg']:
		msg_comp = re.compile(r'^([^:]*):(.*)')
		if msg_comp.match(each_msg):
			each_msg = msg_comp.match(each_msg).groups()
			if "恢复" in each_msg[0]:
				current_info['trigger_state'] = each_msg[0]
				continue
			elif "报警信息如下" in each_msg[0]:
				current_info['trigger_state'] = each_msg[0]
				continue
		else:
			if each_msg:
				each_msg = ['报警内容',each_msg]
		msg.append(each_msg)
	alert_info['msg'] = msg

	current_info['alert_info'] = alert_info
	current_info['img_time'] =alert_detail[0][2]

	acknowleged = zconn.GetEventAcknow(event_id)
	if isinstance(acknowleged,int):
		acknowleged = '0'
	else:
		acknowleged = [time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(acknowleged[0])),acknowleged[1]]
	current_info['acknowleged'] = acknowleged
	current_info['eventid'] = event_id
	current_info['itemid'] = item_id
	return current_info

def HistoryAlert(item_id,zconn):
	history_info = {}
	his = zconn.FromItemidGetAlertHistory(item_id)
	his_detail = []
	unknow=0
	for each in his:
		his_detail.append((time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(each[0])),each[0],each[1],each[2],each[3]))
		if each[1] == 0:unknow+=1

	history_info['his_detail'] = his_detail
	history_info['item_id'] = item_id
	history_info['unknow'] = unknow
	return history_info

def HostTrigger(item_id,zconn):
	host_trigger_info = {}
	host_id = zconn.FromItemidGetHost(item_id)[0][0]
	items = zconn.FromHostidGetItems(host_id)
	onerr = 0
	for each in items:
		if each[2] == 1:onerr+=1
	graphids = zconn.FromHostidGetGraphid(host_id)
	host_trigger_info['graphs'] = graphids
	host_trigger_info['onerr'] = onerr
	host_trigger_info['items'] = items
	return host_trigger_info

def hostimg(request,graphid):
	gf = Base.GetConf()
	import datetime
	stime = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y%m%d%H%M%S')
	curtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	user = gf.getConf('zabbix','user')
	pwd = gf.getConf('zabbix','pwd')
	homepage = gf.getConf('zabbix','homepage')

	url = "%s/chart2.php?graphid=%s&period=604800&stime=%s&" \
	      "updateProfile=1&profileIdx=web.screens&" \
	      "profileIdx2=1363&width=600&screenid=&curtime=%s" % (homepage,graphid,stime,curtime)
	session = requests.Session()
	session.post(homepage,data={'name':user,'password':pwd,'autologin':1,'enter':'Sign in'})
	grf = session.get(url).content
	return HttpResponse(grf,content_type='image/png')


def img(request,stime,itemid):
	gf = Base()
	user = gf.GetConf('zabbix','user')
	pwd = gf.GetConf('zabbix','pwd')
	homepage = gf.GetConf('zabbix','homepage')
	url = "%s/chart.php?period=3600&stime=%s&itemids=%s&width=600" % (homepage,stime,itemid)
	session = requests.Session()
	session.post(homepage,data={'name':user,'password':pwd,'autologin':1,'enter':'Sign in'})
	grf = session.get(url).content
	return HttpResponse(grf,content_type='image/png')