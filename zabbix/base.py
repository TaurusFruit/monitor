import configparser as cf
import os
import logging

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

class SaveLog(Base):
	def __init__(self):
		super(SaveLog,self).__init__()
		try:
			err_log_file = os.path.join(self.GetConf('global','base_dir'),self.GetConf('log','error_log'))
			msg_log_file = os.path.join(self.GetConf('global','base_dir'),self.GetConf('log','msg_log'))
		except Exception as e:
			raise e
		LEVELS = {
		        'debug': logging.DEBUG,
		        'info': logging.INFO,
		        'warning': logging.WARNING,
		        'error': logging.ERROR,
		        'critical': logging.CRITICAL
		    }
		log_level = LEVELS.get(self.GetConf('log','log_level'),logging.INFO)

		err_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

		logging.basicConfig(
		        level=logging.DEBUG,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		datefmt='%a, %d %b %Y %H:%M:%S',
		        filename=err_log_file,
		        filemode='a'

		    )

		#zabbix_wx 日志控制
		self.errlogger = logging.getLogger('zabbix_wx')
		err_handler = logging.FileHandler(err_log_file)
		err_handler.setLevel(log_level)
		err_handler.setFormatter(err_formatter)
		self.errlogger.addHandler(err_handler)

		#msg 日志控制
		self.msglogger = logging.getLogger('wx')
		msg_handler = logging.FileHandler(msg_log_file)
		msg_handler.setLevel(log_level)
		msg_handler.setFormatter(err_formatter)
		self.msglogger.addHandler(msg_handler)




if __name__ == '__main__':
	b = Base()
	print(b.GetConf('mysql','dbhost'))
