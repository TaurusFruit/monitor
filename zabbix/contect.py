'''
用户信息
'''

#用户组信息(对应企业微信后台用户名
Group = {
	2:{
		'name':'admin',
		'users':[
			'zhajx',
			'zhanglei'
		]
	},
	3:{
		'name':'DSP',
		'users':[
			'yangyy',
			'zhaohl',
		]
	},
	4:{
		'name':'Hadoop',
		'users':[
			'lizhang',
		]
	},
	5:{
		'name':"DB",
		'users':[
			'rongtt',
		]
	},
	6:{
		'name':'Aidi',
		'users':[
			'quning',
			'zhuxs',
		]
	},
	7:{
		'name':'SSP',
		'users':[
			'jiaoguangliang'
		]
	}
}

#用户名 对应 真实姓名
User = {
	'diandian':'焦光亮',
	'zhanglei':'张磊',
	'zhajx':'查金星',
	'yangyy':'杨永煜',
	'zhaohl':'赵海龙',
	'lizhang':'李璋',
	'rongtt':'戎彤彤',
	'quning':'曲宁',
	'zhuxs':'朱晓珊',
	'jiaoguangliang':'闫涛',
}

def getUserInfo(username):
	'''
	获取用户组信息
	:param username:
	:return:
	'''
	groupinfo = []
	#判断是否为管理员
	if username in Group[2]['users']:
		for k,v in Group.items():
			if v['name'] != 'admin':
				groupinfo.append(v['name'])
	else:
		for k,v in Group.items():
			if username in v['users']:
				groupinfo.append(v['name'])

	return groupinfo

def getUserGroup(username):
	'''
	获取用户信息
	:param username: 用户名
	:return: 返回用户组ID , 组名
	'''
	for k,v in Group.items():
		if username in v['users']:
			return [k,v['name']]
