'''
Author: lei
Created Time: 2016.7.15
File Name: dbmod.py
Description: zabbix获取数据库方法
'''

import pymysql
import datetime
from .base import Base

class DBMod(Base):
	def __init__(self):
		super(DBMod,self).__init__()
		self.conn = pymysql.connect(
				host=self.GetConf('mysql','dbhost'),
                port=int(self.GetConf('mysql','dbport')),
                user=self.GetConf('mysql','dbuser'),
                passwd=self.GetConf('mysql','dbpassword'),
                db=self.GetConf('mysql','dbname'),
                charset=self.GetConf('mysql','dbcharset'),
               )

	def GetAlertInfo(self,event_id,time_stm=None):
		sql = "SELECT alerts.message,events.clock " \
		      "FROM alerts " \
		      "INNER JOIN events ON alerts.eventid = events.eventid " \
		      "WHERE alerts.eventid=%s " \
		      "GROUP BY events.clock" % event_id
		res = self.execute_sql(sql)
		return res[0][0]


	def GetEventAcknow(self,event_id):
		sql = "SELECT acknowledges.clock,acknowledges.message " \
		      "FROM acknowledges " \
		      "WHERE acknowledges.eventid = %s" % event_id
		res = self.execute_sql(sql)
		if len(res) > 0:
			return res[0]
		else:
			return -1

	# def GetEventAcknow(self,eventid):
	# 	sql = "SELECT acknowledges.clock ,acknowledges.message,users.surname " \
	# 	      "FROM events " \
	# 	      "INNER JOIN acknowledges ON events.eventid=acknowledges.eventid " \
	# 	      "INNER JOIN users on users.userid = acknowledges.userid " \
	# 	      "where events.eventid=%s " \
	# 	      "ORDER BY acknowledges.clock " \
	# 	      "DESC LIMIT 1" % eventid
	# 	rs= self.execute_sql(sql)
	# 	if len(rs) > 0:
	# 		return rs[0]
	# 	else:
	# 		return -1
	#
	# def FromHostidGetGraphid(self,hostid):
	# 	sql = "select graphs_items.graphid,items.key_ " \
	# 	      "from hosts " \
	# 	      "inner join items on items.hostid = hosts.hostid " \
	# 	      "inner join graphs_items on graphs_items.itemid = items.itemid " \
	# 	      "where hosts.hostid=%s " \
	# 	      "and (items.key_ like 'net.if.in[eth%s]' " \
	# 	      "or items.key_ like 'system.cpu.util%s') " \
	# 	      "GROUP BY graphs_items.graphid" % (hostid,'%','%')
	# 	rs = self.execute_sql(sql)
	# 	return rs
	#
	# def __getDay(self,day=1):
	# 	'''
	# 	获取时间段
	# 	:param day:
	# 	:return:
	# 	'''
	# 	if not isinstance(day,int):
	# 		raise "TypeError day must be intter!"
	# 	return [(datetime.datetime.now() - datetime.timedelta(days=int("%s" % day))).strftime('%Y-%m-%d %H:%M:%S'),datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
	#
	#
	# def FromItemidGetAlertHistory(self,itemid,timestamp=2):
	# 	being_time = self.__getDay(timestamp)[0]
	#
	# 	sql = "select events.clock,events.acknowledged,events.eventid,events.value " \
	# 	      "from alerts INNER JOIN events ON alerts.eventid = events.eventid " \
	# 	      "inner join functions on functions.triggerid = events.objectid " \
	# 	      "where  functions.itemid=%s " \
	# 	      "AND events.clock > UNIX_TIMESTAMP('%s') " \
	# 	      "GROUP BY events.eventid " \
	# 	      "ORDER BY events.clock " \
	# 	      "DESC"  % (itemid,being_time)
	# 	rs = self.execute_sql(sql)
	# 	return rs
	#
	# def GetAlertMsg(self,itemid=None,eventid=None):
	# 	if eventid:
	# 		sql = "select users.surname,alerts.message,events.clock " \
	# 		      "from alerts " \
	# 		      "inner join users on alerts.userid=users.userid " \
	# 		      "INNER JOIN events ON alerts.eventid = events.eventid " \
	# 		      "where alerts.eventid=%s" % eventid
	# 	else:
	# 		sql = "select users.surname,alerts.message,events.clock,events.eventid " \
	# 		      "from alerts " \
	# 		      "inner join users on alerts.userid=users.userid " \
	# 		      "INNER JOIN events ON alerts.eventid = events.eventid  " \
	# 		      "inner join functions on functions.triggerid = events.objectid  " \
	# 		      "where " \
	# 		      "functions.itemid=%s " \
	# 		      "GROUP BY events.eventid " \
	# 		      "ORDER BY events.clock " \
	# 		      "desc" % itemid
	#
	# 	rs = self.execute_sql(sql)
	# 	return rs
	#
	# def FromItemidGetHost(self,itemid):
	# 	sql = "SELECT hosts.hostid " \
	# 	      "FROM items " \
	# 	      "INNER JOIN hosts ON hosts.hostid = items.hostid " \
	# 	      "where items.itemid=%s" % itemid
	# 	rs = self.execute_sql(sql)
	# 	return rs
	#
	# def FromHostidGetItems(self,hostid):
	# 	sql = "SELECT triggers.description,items.itemid,triggers.value,max(events.eventid) " \
	# 	      "FROM items " \
	# 	      "INNER JOIN functions ON functions.itemid = items.itemid " \
	# 	      "INNER JOIN triggers ON triggers.triggerid = functions.triggerid " \
	# 	      "INNER JOIN events ON events.objectid = functions.triggerid " \
	# 	      "WHERE items.hostid= %s " \
	# 	      "AND triggers.status=0 " \
	# 	      "GROUP BY triggers.description" % hostid
	# 	rs = self.execute_sql(sql)
	# 	return rs
	#
	def FromEventidGetItemid(self,event_id):
		'''
		通过eventid获取itemid
		:param eventid:
		:return:
		'''
		sql = "SELECT functions.itemid FROM events " \
		      "INNER JOIN functions ON functions.triggerid = events.objectid " \
		      "WHERE eventid = %s" % event_id
		rs = self.execute_sql(sql)
		if len(rs) > 0:
			return rs[0][0]
		else:
			return -1

	def execute_sql(self,sql):
		'''
		执行sql语句
		:param sql:sql 语句
		:return:
		'''
		cursor = self.conn.cursor()
		try:
			cursor.execute(sql)
			return cursor.fetchall()
		except Exception as e:
			print(e)
			return ''
		finally:
			cursor.close()

if __name__ == '__main__':
	d = DBMod()
	print(d.FromEventidGetItemid(489377))
