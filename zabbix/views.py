from django.shortcuts import render,HttpResponse
import requests
import time
import re
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token
import datetime
from .base import Base
from .dbmod import DBMod
from .WXBizMsgCrypt import WXBizMsgCrypt
from .zabbix_api import ZabbixApi
from django.utils.encoding import smart_str
import xml.etree.cElementTree as ET
from . import contect

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

	#数据库连接方法
	dbconn = DBMod()
	#项目ID
	item_id = dbconn.FromEventidGetItemid(event_id)

	#当前报警信息
	current_alert_info = CurrentAlertInfo(event_id,dbconn)
	history_alert_info = HistoryAlertInfo(item_id,dbconn)
	host_trigger_info = HostTriggerInfo(item_id,dbconn)

	return render(request, 'zabbix/alert_info.html', {'current_info':current_alert_info,
	                                                  'history_info':history_alert_info,
	                                                  'hosttrigger_info':host_trigger_info
	                                                  }
	              )

def HostNewrok(request,group_name,eth_id):
	'''
	通过主机组名获取主机流量图
	:param request:
	:param group_name:
	:return:
	'''
	dbconn = DBMod()
	host_eth_ids = dbconn.FromGroupidGetHostEthid(group_name)
	return render(request,'zabbix/host_network.html',{'host_eth_id':host_eth_ids,'eth_id':eth_id})

def HostLoad(request,group_name):
	'''
	通过主机组名获取主机负载图
	:param request:
	:param group_name:
	:return:
	'''
	dbconn = DBMod()
	host_load_ids = dbconn.FromGroupidGetHostLoadid(group_name)
	return render(request,'zabbix/host_load.html',{'host_load_id':host_load_ids})



def HostTriggerInfo(item_id,dbconn):
	host_trigger_info = {}.fromkeys(['items'],0)
	#获取主机ID
	host_id = dbconn.FromItemidGetHost(item_id)[0][0]
	#获取主机项目列表, [触发器名称,项目ID,触发器状态,最新事件ID]
	item_list = dbconn.FromHostidGetItems(host_id)
	onerr = 0
	for each in item_list:
		if each[2] == 1:
			onerr +=1
	host_trigger_info['onerr'] = onerr
	host_trigger_info['items'] = item_list
	#获取图形ID
	graphs = dbconn.FromHostidGetGraphid(host_id)
	host_trigger_info['graphs'] = []
	for each in graphs:
		host_trigger_info['graphs'].append(each[0])

	print(host_trigger_info['graphs'])

	return host_trigger_info


def HistoryAlertInfo(item_id,dbconn):
	'''
	获取当前项目历史报警记录
	:param item_id: 项目ID
	:param dbconn: 数据库连接方法
	:return:
	'''
	item_history_info = {}.fromkeys(['item_id','his_detail'],0)
	item_history_info['item_id'] = item_id

	#获取项目历史记录,返回 (时间,是否知悉,事件ID,报警类型)
	history_detail = dbconn.FromItemidGetAlertHistory(item_id)
	#item_history_info['his_detail'] 返回报警详细信息
	#格式 [时间戳,是否知悉,事件ID,报警类型,可读时间]
	item_history_info['his_detail'] = []
	unknow = 0
	for each in history_detail:
		each = list(each)
		if each[1] == 0:
			unknow +=1
		time_stm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(each[0])))
		each.append(time_stm)
		item_history_info['his_detail'].append(each)
	item_history_info['unknow'] = unknow
	return  item_history_info

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
	'''
	正确返回格式: alert_msg_info = (时间,信息内容)
	'''
	alert_msg_info = dbconn.GetAlertInfo(event_id)

	#如果获取错误返回-1
	if alert_msg_info == -1:
		return -1

	#配置图片时间
	current_alert_info['img_time'] = alert_msg_info[1]
	alert_msg = alert_msg_info[0]

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

	#判断是否知悉
	#如果ack_msg == -1 表示未知晓
	if ack_msg == -1:
		current_alert_info['acknowleged'] = 0
	else:
		#ack_msg = [知悉时间,知悉内容]
		ack_msg = list(ack_msg)
		ack_msg[0] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(ack_msg[0])))
		current_alert_info['acknowleged'] = list(ack_msg)

	#配置event_id
	current_alert_info['event_id'] = event_id
	#配置item_id
	current_alert_info['itemid'] = dbconn.FromEventidGetItemid(event_id)

	return current_alert_info

def hostimg(request,graphid):
	gf = Base()
	stime = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y%m%d%H%M%S')
	curtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	user = gf.GetConf('zabbix','user')
	pwd = gf.GetConf('zabbix','pwd')
	homepage = gf.GetConf('zabbix','homepage')

	url = "%s/chart2.php?graphid=%s&period=604800&stime=%s&" \
	      "updateProfile=1&profileIdx=web.screens&" \
	      "profileIdx2=1363&width=600&screenid=&curtime=%s" % (homepage,graphid,stime,curtime)
	session = requests.Session()
	session.post(homepage,data={'name':user,'password':pwd,'autologin':1,'enter':'Sign in'})
	grf = session.get(url).content
	return HttpResponse(grf,content_type='image/png')

def cacti_graf(request):
	host = request.GET.get('host')
	r_id = request.GET.get('r_id')
	if not r_id:r_id=1
	if host == 'linli':
		url = "http://monitor.cnnix.cn/index.php"
		user = "hzts"
		pwd = "hzts"
		img_url = "http://monitor.cnnix.cn/graph_image.php?action=view&local_graph_id=3169&rra_id=%s" % r_id
	elif host == 'baoshun':
		url = "http://123.59.7.152/cacti/index.php"
		user = "zhangl"
		pwd = "zhangl123456"
		img_url = "http://123.59.7.152/cacti/graph_image.php?action=view&local_graph_id=3019&rra_id=%s" % r_id
	data = {'action':'login','login_username':user,'login_password':pwd}
	session = requests.Session()
	session.post(url,data)
	graf = session.get(img_url).content
	return HttpResponse(graf,content_type="image/png")

def img(request,stime,itemid):
	'''
	显示图片信息
	:param request:
	:param stime: 时间戳
	:param itemid: 项目ID
	:return:
	'''
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

@csrf_exempt
def wx_api(request):
	gf = Base()
	# sToken = config.tokend_config['sToken']
	sToken = gf.GetConf('tokend','stoken')
	# sEncodingAESKey = config.tokend_config['sEncodingAESKey']
	sEncodingAESKey = gf.GetConf('tokend','sencodingaeskey')
	# sCorpID = config.tokend_config['corpid']
	sCorpID = gf.GetConf('tokend','corpid')

	wxcpt=WXBizMsgCrypt(sToken,sEncodingAESKey,sCorpID)

	if request.method == 'GET':
		return _wx_get(request,wxcpt)
	elif request.method == 'POST':
		return _wx_post(request,wxcpt)


#GET数据
def _wx_get(request,wxcpt):
	msg_signature = request.GET.get('msg_signature')
	timestamp = request.GET.get('timestamp')
	nonce = request.GET.get('nonce')
	echostr = request.GET.get('echostr')
	ret,sEchoStr=wxcpt.VerifyURL(msg_signature, timestamp,nonce,echostr)
	if(ret!=0):sEchoStr='Error'
	return HttpResponse(sEchoStr)

#POST数据，解密
@csrf_exempt
def _wx_post(request,wxcpt):
	path = request.get_full_path()
	print(path)

	sReqData = request.body
	print(sReqData)

	sReqMsgSig,sReqTimeStamp,sReqNonce = _path_pars(path)

	ret,sMsg=wxcpt.DecryptMsg( sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
	print(ret,sMsg)
	if (ret!=0):
		return HttpResponse('ERROR')
	xml_tree = ET.fromstring(sMsg)
	MsgType = xml_tree.find("MsgType").text
	print(MsgType)

	Msg_dick = _xml_pars(sMsg)
	print(Msg_dick)

	ResContent = ''

	if MsgType == 'event':
		if Msg_dick['Event'] == 'click':#
			if Msg_dick['EventKey'] == 'show_help':
				ResContent = _show_help(Msg_dick['FromUserName'])
			elif 'traf' in Msg_dick['EventKey'] or 'load' in Msg_dick['EventKey'] :
				if 'traf' in Msg_dick['EventKey'] :
					tag = 'traf'
				elif 'load' in Msg_dick['EventKey'] :
					tag = 'load'

				group_name = Msg_dick['EventKey'].split('_')[1]
				ResContent = _show_group_graf(Msg_dick['FromUserName'],group_name,tag)


	res = ResData(wxcpt,Msg_dick['ToUserName'],Msg_dick['FromUserName'],Msg_dick['CreateTime'],ResContent,sReqNonce,sReqTimeStamp)
	return HttpResponse(res)

def _show_group_graf(username,groupname,tag):
	'''
	获取流量图信息
	:param username:
	:param groupname:
	:return:
	'''
	contect_info = contect.getUserGroup(username)
	if username in contect.User.keys() :
		real_name = contect.User[username]
	else:
		return "您好,你还没有相关权限,请联系管理员."
	if groupname not in contect_info and 'admin' not in contect_info:
		return "%s 你好,你没有查看 %s 组 权限,请联系管理员" % (real_name,groupname)
	if tag == 'traf':
		msg = "%s 你好,查看 %s 主机组流量图请点击: <a href='http://zabbix.tansuotv.cn/wx_api/network/%s/1'>eth1</a>" \
	      "查看<a href='http://zabbix.tansuotv.cn/wx_api/network/%s/0'>eth0</a>" % (real_name,groupname,groupname,groupname)
	elif tag == 'load':
		msg = "%s 你好,查看 %s 主机负载图请点击: <a href='http://zabbix.tansuotv.cn/wx_api/load/%s'>点击</a>" (real_name,groupname,groupname)

	return msg


def _show_help(username):
	msg = "%s 你好\n点击报警报警信息可进入报警详情页面\n在报警详情页面可以进行知悉事件操作\n" % contect.User[username]
	return  msg

#获取url数据
def _path_pars(path):
	path_list = []
	for each in path.split('?')[1].split('&'):
		path_list.append(each.split('=')[1])
	return path_list

#测试分析xml
def _xml_pars(content):
	msg_xml = ET.fromstring(content)
	msg = {}
	for element in msg_xml:
		msg[element.tag] = smart_str(element.text)
	return msg


#返回文字数据
def ResData(wxcpt,ToUserName,FromUserName,CreateTime,Content,sReqNonce,sReqTimeStamp):
	sRespData = "<xml>" \
	            "<ToUserName><![CDATA[%s]]></ToUserName>" \
	            "<FromUserName><![CDATA[%s]]></FromUserName>" \
	            "<CreateTime>%s</CreateTime>" \
	            "<MsgType><![CDATA[text]]></MsgType>" \
	            "<Content><![CDATA[%s]]></Content></xml>" % (ToUserName,FromUserName,CreateTime,Content)
	ret,sEncryptMsg=wxcpt.EncryptMsg(sRespData, sReqNonce)
	if ret!=0:
		return "ERROR"
	return sEncryptMsg
