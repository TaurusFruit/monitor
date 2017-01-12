from django.conf.urls import  url
from . import views

urlpatterns = [
	url(r'^wx_api/test.html$',views.test),
	url(r'^wx_api/alert_info/(?P<event_id>\d+)/(?P<time_stm>\d+)?$',views.AlertInfo),
	url(r'^wx_api/img/(?P<stime>\d+)/(?P<itemid>\d+)',views.img),
	# url(r'^wx_api/cacti_graf',views.cacti_graf),
]
