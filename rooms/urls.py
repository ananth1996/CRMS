from django.conf.urls import url,include
from rooms.views import addVenue, viewVenue,editVenue,addEquip,addDept,bookVenue,venue_list,appovalView,approvalVenue,addRes

urlpatterns =[
	url(r'^addVenue/$',view=addVenue.as_view(),name = 'addVenue'),
	url(r'^viewVenue/$',view=venue_list, name='viewVenue'),
	url(r'editVenue/(?P<venue_id>[0-9]+)/$',view=editVenue.as_view(),name='editVenue'),
	url(r'^addEquip/$',view=addEquip.as_view(),name = 'addEquip'),
	url(r'^addRes/$', view=addRes.as_view(), name='addRes'),
	url(r'addDept/$',view=addDept.as_view(),name='addDept'),
	url(r'bookVenue/(?P<venue_id>[0-9]+)/(?P<startdate>\d{4}-\d{2}-\d{2})/(?P<enddate>\d{4}-\d{2}-\d{2})$',view=bookVenue.as_view(),name='bookVenue'),
	url(r'^approval/$',view=appovalView.as_view(),name='approvalView'),
	url(r'approvalVenue/(?P<venue_id>[0-9]+)/$',view=approvalVenue.as_view(),name='approvalVeneu'),
]