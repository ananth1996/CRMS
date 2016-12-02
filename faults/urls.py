from django.conf.urls import url, include
from faults.views import *

urlpatterns = [
		url(r'^addFault/$',view=addFault.as_view(),name='addFault'),
		url(r'^viewFault/$',view=viewFault, name='viewFault'),
	    url(r'editFault/(?P<fault_id>[0-9]+)/$',view=editFault.as_view(),name='editFault')
                ]
