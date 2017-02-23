'''
Author: lei
Created Time: 2016.7.8
File Name: JsonZabbixAPI
Description:存储Zabbix API json格式
'''

def JsonDict(jname,token,keys=None,time_from=None,time_till=None,eventids=None,actionids=None,hostids=None,triggerids=None):
	method = {
		#获取指定ID主机
		'hostname_get':{
			'method':'host.get',
			'params':{
				'output':['name'],
				'filter':{
					'hostid':hostids
				}
			}
		},

		#获取全部主机
		'hostget':{
			'method':'host.get',
			'params':{
				'output':['name'],
			}
		},
		#获取主机主机组关系
		'hostofgroup':{
			'method':'host.get',
			'params':{
				"output": ["hostid"],
				"selectGroups": ['groupid'],
				'filter':{
					'hostid':[]
				}
			}
		},
		#获取主机组信息
		'groupget':{
			'method':'hostgroup.get',
			'params':{
				"output": ['name'],
			}
		},
		#获取项目信息
		'itemget':{
			"method": "item.get",
			"params": {
				"output": ['key_','lastvalue'],#"extend",
				"hostids": hostids ,
				"sortfield": "name",
				"search":{
					"key_" :keys
				},

			},
		},
		#获取触发器-itemid
		'triggerget':{
			"method": "trigger.get",
			"params":{
				"triggerids": triggerids,
				"output": "extend",
                "selectFunctions": "extend"
			}
		},


	}

	json_data = {
		"jsonrpc":"2.0",
		"auth":token, # the auth id is what auth script returns, remeber it is string
		"id":1,
	}
	method[jname].update(json_data)
	return method[jname]
