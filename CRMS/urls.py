# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$',views.slash,name='splash'),
    url(r'^home/', views.Home.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
	url(r'^print/booking/(?P<bookid>\d+)',views.printBook,name="printBook"),
	url(r'^print/req/(?P<reqid>\d+)',views.printreq,name="printreq"),
	url(r'^rooms/',include('rooms.urls')),
    url(r'^log/', include('log.urls')),
	url(r'faults/',include('faults.urls')),
	url(r'req/',include('req.urls')),
	url(r'print/schedule/(?P<start>\d{4}-\d{2}-\d{2})/(?P<end>\d{4}-\d{2}-\d{2})$',view=views.printSchedule,name='schedulePrint'),
	url(r'print/faults/',view=views.printFault,name='printfault'),
	url(r'cancel/(?P<bookid>\d+)',view=views.cancelBook,name='cancelBook')
   ]

admin.site.site_header = u'R³ Management Administration'
