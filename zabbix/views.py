from django.shortcuts import render,HttpResponse
import requests
import time
import re
from .base import Base
from .dbmod import DBMod
from .zabbix_api import ZabbixApi

# Create your views here.


def test(request):
	return HttpResponse('ok')

def AlertDetail(request,event_id,time_stm):
	'''
	通过 事件ID 时间戳 获取当前报警详情
	url ex:  http://zabbix.coom/wx_api/alert_detail/123213/
	:param event_id: 事件ID
	:param time_stm: 时间戳
	:return 返回报警详情页
	'''
	#项目ID
	# item_id = DBMod.FromEventidGetItemid(event_id)

	#数据库连接方法
	dbconn = DBMod()

	#当前报警信息
	current_alert_info = CurrentAlertInfo(event_id,dbconn)

	return render(request, 'zabbix/alert_info.html', {'current_info':current_alert_info})


def CurrentAlertInfo(event_id,dbconn,time_stm=None):
	'''
	获取当前时间戳报警详情
	:param event_id: 事件ID
	:param dbconn: 数据库连接方法
	:param time_stm: 时间戳
	:return:
	'''
	#报警详细信息
	current_alert_info = {}.fromkeys(['alert_info','status','acknowleged','event_id'],1)


	#获取事件报警信息
	alert_msg = dbconn.GetAlertInfo(event_id)
	#如果获取错误返回-1
	if not alert_msg: return -1
	#格式化报警信息
	alert_msg = alert_msg.replace('\r','').replace('\\r\\n','\n').replace('：',':').split('\n')
	alert_msg.pop(0)
	current_alert_info['alert_info'] = []
	for each in alert_msg:
		if len(each) < 1:pass
		each = each.split(':')
		current_alert_info['alert_info'].append(each)

	#获取事件知悉情况
	ack_msg = dbconn.GetEventAcknow(event_id)
	#配置图片时间
	current_alert_info['img_time'] = ack_msg[0]
	#判断是否知悉
	if ack_msg == -1:
		current_alert_info['acknowleged'] = 0
	else:
		ack_msg = list(ack_msg)
		ack_msg[0] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(ack_msg[0])))
		current_alert_info['acknowleged'] = list(ack_msg)

	#配置event_id
	current_alert_info['event_id'] = event_id
	#配置item_id
	current_alert_info['itemid'] = dbconn.FromEventidGetItemid(event_id)

	return current_alert_info

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


def SetAcknowlege(request):
	'''
	通过zabbix api提交知悉内容
	:param request:
	:return:
	'''
	zabbix_api = ZabbixApi()
	event_id = request.GET.get('eventid')
	confirm_msg = request.GET.get('msg')
	zabbix_api.acknow(event_id,confirm_msg)
	return HttpResponse('ok')