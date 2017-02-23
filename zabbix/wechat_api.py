'''
定义微信方法
'''



class WechatCmd(object):
	def __init__(self):
		self.command_list = ['help']
		for each in ['dsp','aidi','had','ssp','db']:
			self.command_list.append("traf_%s" % each)
			self.command_list.append("load_%s" % each)





if __name__ == '__main__':
	w = WechatCmd()
	print(w.command_list)



