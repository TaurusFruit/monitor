from django.conf.urls import  url
from . import views

urlpatterns = [
	#测试页
	url(r'^wx_api/test.html$',views.test),
	#报警详情页
	url(r'^wx_api/alert_detail/(?P<event_id>\d+)/(?P<time_stm>\d+)?$',views.AlertDetail,name='alertdetail'),
	#知悉提交
	url(r'^wx_api/acknowlege.html',views.SetAcknowlege),
	#显示图片内容
	url(r'^wx_api/img/(?P<stime>\d+)/(?P<itemid>\d+)',views.img,name='img'),
	#显示主机图片内容
	url(r'^wx_api/hostimg/(?P<graphid>\d+)',views.img),
	url(r'^wx_api/hostimg/(?P<graphid>\d+)',views.hostimg,name='hostimg'),

	# url(r'^wx_api/img/(?P<stime>\d+)/(?P<itemid>\d+)',views.img),
	url(r'^wx_api/cacti_graf',views.cacti_graf),

	#微信api
	url(r'^wx_api/api.py',views.wxapi),
]
