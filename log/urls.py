from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from . import views
from forms import LoginForm

urlpatterns = [
	
	url(r'^login/$',views.User_login,name='login'),
	url(r'^logout/$',views.User_logout.as_view(),name='logout'),
	url(r'addStud/$',views.addStud.as_view(),name='addStud'),
	url(r'addFac/$',views.addFac.as_view(),name='addFac'),
	url(r'addPer/$', views.addPer.as_view(), name='addPer')

]
