from django import forms
from rooms.models import FacultyBook,StudentBook,Bookrequest
from datetimewidget.widgets import DateWidget

class PrintForm(forms.Form):
	starttime = forms.DateTimeField(required=True, widget=DateWidget(usel10n=True, bootstrap_version=3),label="StartDate")
	endtime = forms.DateTimeField(required=True, widget=DateWidget(usel10n=True, bootstrap_version=3),label="EndDate")
