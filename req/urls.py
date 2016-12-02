from django.conf.urls import url,include
from .views import addEquipReq,editReq,viewReq

urlpatterns =[
	url(r'^addReq/$',view=addEquipReq.as_view(),name = 'addEquip'),
	url(r'^viewReq/$',view=viewReq, name='viewReq'),
	url(r'editReq/(?P<req_id>[0-9]+)/$', view=editReq.as_view(), name='editReq')

]