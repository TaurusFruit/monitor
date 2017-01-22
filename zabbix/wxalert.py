'''
Author: lei
Created Time: 2016.7.25
File Name: WXAlert.py
Description: 微信接口,发送消息
'''


import requests
import json

from . import dbmod
from .base import *

class WXAlert(SaveLog):
	def __init__(self,toparty,content):
		super(WXAlert,self).__init__()
		self.toparty = toparty
		self.content = content

		dbconn = dbmod.DBMod()

		self.gettoken_id = {
			'corpid' :self.GetConf('tokend','corpid'),
			'corpsecret' : self.GetConf('tokend','corpsecret')
		}

		self.gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'     #获取AccessToken 地址,获取方式get

		#文字内容
		self.main_content = {
			'toparty':toparty,          #部门ID
			'msgtype':'text',           #发送模式
			'agentid':1,                #应用ID
			'text':{
				'content':content       #消息内容
			}
		}

		#获取事件ID
		event_id = self.__contentPars

		img_time = dbconn.GetAlertInfo(event_id)[1]

		self.new_content = {
			'toparty':toparty,
			'msgtype':'news',
			'agentid':1,
			'news':{
				'articles':[
					{
						'title':'您有新的报警',
						'description':content,
						'picurl':"%s/wx_api/img/%s/%s" % (self.GetConf('zabbix','homepage'),img_time,event_id),
						'url':'%s/wx_api/alert_detail/%s/' % (self.GetConf('zabbix','homepage'),event_id)
					},
				]
			}
		}

	def getToken(self):
		for k,v in self.gettoken_id.items():
			self.gettoken_url += '%s=%s&' % (k,v)
		response = requests.get(self.gettoken_url)
		token = response.json()['access_token']
		return token

	def uploadImg(self,imgPath):
		files = {'file':(open(imgPath,'rb'))}
		url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image" % (self.getToken())
		res = requests.post(url,files=files)
		return res.json()

	def sendMsg(self):
		url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % (self.getToken())
		ret = requests.post(url,json.dumps(self.new_content,ensure_ascii=False).encode('utf8'))
		self.msglogger.info(self.new_content)

	@property
	def __contentPars(self):
		for each in self.content.split("\n"):
			if "ID" in each:
				return int(each.split()[-1])
		else:
			return False

