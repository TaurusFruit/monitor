import configparser as cf
import os

class Base(object):
	'''
	基础类,获取配置信息
	'''
	def __init__(self):
		self.conf_file = os.path.join(os.curdir,'zabbix/conf.ini')
		self.config = cf.ConfigParser()
		self.config.read(self.conf_file)


	def GetConf(self,conf_name,keyword):
		return self.config.get(conf_name,keyword)




if __name__ == '__main__':
	b = Base()
	print(b.GetConf('mysql','dbhost'))
