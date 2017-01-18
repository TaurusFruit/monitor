import requests
import json
from .base import Base

class ZabbixApi(Base):
	'''
	zabbix api 类方法
	'''
	def __init__(self):
		super(ZabbixApi,self).__init__()
		self.header = {"Content-Type": "application/json"}
		self.user = self.GetConf('zabbix','user')
		self.pwd = self.GetConf('zabbix','pwd')
		self.url = self.GetConf('zabbix','homepage') + "/api_jsonrpc.php"
		self.token = self.getToken()

	def __RequestPost(self,data):
		request = requests.post(self.url,data=json.dumps(data),headers=self.header)
		try:
			return json.loads(request.text)['result']
		except Exception as e:
			return json.loads(request.text)

	def getToken(self):
		token = {
			"jsonrpc": "2.0",
			"method": "user.login",
			"params": {
				"user": self.user,
				"password": self.pwd
			},
			"id": 0
		}
		res = self.__RequestPost(token)
		if res == -1:
			return -1
		else:
			return res

	def acknow(self,event_id,confirm_msg="微信确认"):
		data = {
			"jsonrpc": "2.0",
			"method": "event.acknowledge",
			"params": {
			    "eventids": event_id,
			    "message": confirm_msg,
			},
			"auth": self.token,
			"id": 1
			}


		print(self.token)
		print(data)
		print(self.__RequestPost(data))
