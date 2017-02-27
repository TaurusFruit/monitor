import requests
import json
from .zabbix_jason import JsonDict
from .base import Base
import re

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

	def getGroupID(self,groupname):
		'''
		获取主机组ID
		:param groupname: 主机组名
		:return: 主机组ID
		'''
		data = {
			"jsonrpc": "2.0",
			"method": "hostgroup.get",
			"params": {
				"output": "extend",
				"filter": {
					"name": [
						groupname
					]
				}
			},
			"auth": self.token,
			"id": 1
		}
		res = self.__RequestPost(data)
		if res == -1:
			return -1
		else:
			return res[0]['groupid']

	def getGroupHost(self,groupid):
		'''
		获取相应主机组全部主机组信息
		:return:
		'''
		all_host = []
		#获取全部主机/主机组关系
		data = 	{
			'jsonrpc':'2.0',
			'method':'host.get',
			'params':{
				"output": ['name','hostid'],
				'groupids':groupid,

			},
			'auth':self.token,
			'id':1
		}
		res = self.__RequestPost(data)
		for each in res:
			if re.match(r'^\d+',each['name']):
				all_host.append(each)
		return all_host

	def getHostNetItemid(self,hostid,type):
		'''
		获取主机网卡item id
		:param hostid:
		:return:
		'''

		items_info = []
		item_id_data = {
		    "jsonrpc": "2.0",
		    "method": "item.get",
		    "params": {
		        "output": ["key_"],
		        "hostids": hostid,
		        "search": {
		            "key_": "net.if.%s" % type
		        },
		        "sortfield": "name"
		    },
		    "auth": self.token,
		    "id": 1
		}
		res = self.__RequestPost(item_id_data)
		if res != -1:
			for each in res:
				if 'eth' in each['key_']:
					items_info.append(each)
		return items_info

	def getItemHistory(self,itemid):
		'''
		获取项目历史记录
		:param itemid:
		:return:
		'''
		item_history_data = {
		   "jsonrpc":"2.0",
		   "method":"history.get",
		   "params":{
		       "output":"extend",#["value"],
		       "history":3,
			   "sortfield": "clock",
               "sortorder": "DESC",
		       "itemids":itemid,
		       "limit":1440
		   },
		   "auth":self.token,
		   "id":1,
		}
		res = self.__RequestPost(item_history_data)
		return  res

	def getGroupTraffID(self,group_name,flag):
		'''
		获取主机组中主机网卡item ID
		:param group_name:
		:param flag:
		:return:
		'''
		pass



	def getGroupAvgTraff(self,group_name,flag):
		'''
		获取主机平均流量信息
		:param type:
		:return:
		'''
		#获取主机组ID
		group_id = self.getGroupID(group_name)

		#获取主机组中主机ID以及主机名称
		host_of_group =  self.getGroupHost(group_id)

		#主机ID,名称表
		host_info = {}
		for each in host_of_group:
			host_info[each['hostid']] = each['name']

		print(host_info)

		for each in host_info.keys():
			item_ids = self.getHostNetItemid(each,flag)
			print(item_ids)

		#获取主机对应item id 历史记录
		host_net_itemid_info = {}
		host_eth0_info = {}
		host_eth1_info = {}
		# for each in host_info.keys():
		# 	item_ids = self.getHostNetItemid(each,flag)
		# 	try:
		# 		eth0_id = item_ids[0]['itemid']
		# 		eth1_id = item_ids[1]['itemid']
		# 	except:
		# 		return 0
		# 	eth0_his = self.getItemHistory(eth0_id)
		# 	eth1_his = self.getItemHistory(eth1_id)
		# 	eth0_totle = 0
		# 	num = 0
		# 	for i in eth0_his:
		# 		eth0_totle += int(i['value'])
		# 		num += 1.0
		# 	eth0_avg = int(eth0_totle/num)
		#
		# 	eth1_totle = 0
		# 	num = 0
		# 	for i in eth1_his:
		# 		eth1_totle+= int(i['value'])
		# 		num += 1.0
		# 	eth1_avg = int(eth1_totle/num)
		# 	host_eth0_info[each] = eth0_avg
		# 	host_eth1_info[each] = eth1_avg
		#
		# host_eth0_info = sorted(host_eth0_info.items(),key=lambda x:x[1],reverse=True)
		# host_eth1_info = sorted(host_eth1_info.items(),key=lambda x:x[1],reverse=True)
		# host_eth0_detail = []
		# host_eth1_detail = []
		#
		# for i in host_eth0_info:
		# 	unit = ['b','kb','mb','gb']
		# 	unit_tag = 0
		# 	eth0_traf = i[1]
		# 	while eth0_traf > 1024:
		# 		eth0_traf /= 1024
		# 		unit_tag += 1
		# 	eth0_traf = "%.2f %s" % (eth0_traf,unit[unit_tag])
		# 	host_eth0_detail.append((host_info[i[0]],eth0_traf))
		#
		# for i in host_eth1_info:
		# 	unit = ['b','kb','mb','gb']
		# 	unit_tag = 0
		# 	eth1_traf = i[1]
		# 	while eth1_traf > 1024:
		# 		eth1_traf /= 1024
		# 		unit_tag += 1
		# 	eth1_traf = "%.2f %s" % (eth1_traf,unit[unit_tag])
		# 	host_eth1_detail.append((host_info[i[0]],eth1_traf))
		#
		# res = ""
		# for each in range(len(host_eth1_detail)):
		# 	res += "%s:\teth0:%s\teth1:%s\n" % (host_eth1_detail[each][0],host_eth0_detail[each][1],host_eth1_detail[each][1])
		# # res = host_eth0_detail
		# #
		# return res
		#
		#
		#
		# # eth0_traff_info  = sorted(host_eth0_info.items(),key=lambda d:d[0],reversed=True)
		#
		# # print(eth0_traff_info)
		#
		# #返回两个字典,分别是eth0,eth1的值




	def acknow(self,event_id,confirm_msg="微信确认"):
		'''
		确认时间信息
		:param event_id:
		:param confirm_msg:
		:return:
		'''
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

	def getGroupTraff(self,groupname):
		'''

		- 获取主机组流量信息
			1. 通过主机组获取所有组内的 主机ID 主机名
			2. 通过主机ID 获取相应的网卡项目ID
			3. 通过网卡项目ID 获取 相应的流量信息

		:return:
		'''
		pass
