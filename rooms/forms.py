from django import forms
from django.db.models import Q
from rooms.models import Venue,Equipment,Bookrequest,VenueEquipment
from log.models import Department
from django.contrib.admin.widgets import AdminSplitDateTime
from datetimewidget.widgets import DateTimeWidget,DateWidget
from django_filters import widgets
import django_filters
from datetime import timedelta


class venueForm(forms.ModelForm):

	class Meta:
		model = Venue
		fields = ['venuename','venueid','dno','capacity']

	def __init__(self,*args,**kwargs):
		super(venueForm, self).__init__(*args, **kwargs)
		self.fields['venuename'].required = True
		self.fields['dno'].required = True
		self.fields['capacity'].required = True
		self.fields['venueid'].disabled = True
		self.fields['capacity'] = forms.IntegerField(min_value=1)
		print self.fields['capacity'].min_value
		venue=Venue.objects.order_by('-venueid')
		if venue:
			self.fields['venueid'].initial = venue[0].venueid +1
		else:
			self.fields['venueid'].initial = 0


class editForm(forms.ModelForm):

	class Meta:
		model = Venue
		fields = ['venuename','capacity']

	def __init__(self,*args,**kwargs):
		super(editForm, self).__init__(*args, **kwargs)
		self.fields['venuename'].disabled = True
		self.fields['capacity'].required = True


class equipForm(forms.ModelForm):

	class Meta:
		model = Equipment
		fields = ['etypeid','ename']

	def __init__(self,*args,**kwargs):
		super(equipForm, self).__init__(*args, **kwargs)
		self.fields['etypeid'].disabled = True
		self.fields['ename'].required = True
		id = Equipment.objects.order_by('-etypeid')
		if id:
			self.fields['etypeid'].initial = id[0].etypeid + 1
		else:
			self.fields['etypeid'].initial = 0


class addDeptFor(forms.ModelForm):
	class Meta:
		model = Department
		fields = ['dno','dname']

	def __init__(self,*args,**kwargs):
		super(addDeptFor, self).__init__(*args, **kwargs)
		self.fields['dno'].disabled = True
		self.fields['dname'].required = True
		id = Department.objects.order_by('-dno')
		if id:
			self.fields['dno'].initial = id[0].dno + 1
		else:
			self.fields['dno'].initial = 0



class bookVenueForm(forms.ModelForm):

	def __init__(self,*args,**kwargs):
		#venue_id = kwargs.pop('venue_id',None)
		super(bookVenueForm, self).__init__(*args, **kwargs)
		#self.fields['venueid'].queryset = Venue.objects.filter(dno=Venue.objects.get(pk=venue_id).dno)
		self.fields['idbookrequest'].label = "Booking ID"
		id=Bookrequest.objects.order_by('-idbookrequest')
		if id:
			self.fields['idbookrequest'].initial = id[0].idbookrequest +1
		else:
			self.fields['idbookrequest'].initial = 0

		self.fields['idbookrequest'].disabled =True



	class Meta:
		model = Bookrequest
		fields=['idbookrequest','venueid','starttime','endtime']
		widgets={'starttime': DateTimeWidget(usel10n=True, bootstrap_version=3),
				'endtime': DateTimeWidget(usel10n=True, bootstrap_version=3)
				 }




class VenueFilter(django_filters.FilterSet):
	equipment = django_filters.ModelChoiceFilter(queryset= Equipment.objects.filter(etypeid__gte=0),method='custom')
	capacity = django_filters.NumberFilter(lookup_expr='gte')
	startdate = django_filters.DateTimeFilter(name="Date Start",widget=DateTimeWidget(usel10n=True, bootstrap_version=3),method='dateStartFilter')
	enddate = django_filters.DateTimeFilter(name="Date Start",widget=   DateTimeWidget(usel10n=True, bootstrap_version=3),method='dateEndFilter')

	def __init__(self, *args, **kwargs):
		super(VenueFilter, self).__init__(*args, **kwargs)
		#getting the options for departmets

		'''
		qs = Venue._default_manager.distinct()
		qs = qs.order_by("dno__dname").values_list("dno__dname", flat=True)
		#adding the choices to the filter
		CHOICES = [(s, s) for s in qs]
		#adding an extra choice of selecting all departments
		CHOICES.insert(0, ('', 'All Departments'))
		library = django_filters.ChoiceFilter(
			name="dno__dname",
			choices=CHOICES,
			widget=widgets.LinkWidget,
		)
		#setting the filter for Department Number to the filter descibed above
		self.filters['dno'] = library
		'''

		#easier Method to add an extra field



	#  a custom function for handling the equipment drop down menue
	def custom(self, queryset, name, value):
		# construct the full lookup expression
		return queryset.filter(venueid__in=VenueEquipment.objects.filter(etypeid=value.etypeid,quantity__gt=0).values('venueid'))

	def dateStartFilter(self,queryset,name,value):
		#print name,value,type(value)
		booked_venues=Bookrequest.objects.filter(starttime__lt=value,endtime__gt=value)
		#print "Time greate ",booked_venues
		booked_venues = booked_venues.filter(Q(status=Bookrequest.APPROVED))
		#print "Approved",booked_venues
		return queryset.filter(~Q(venueid__in=booked_venues.values('venueid')))

	def dateEndFilter(self,queryset,name,value):
		#print name,value,type(value)
		booked_venues=Bookrequest.objects.filter(endtime__gt=value,starttime__lt=value)
		#print "Time greate ",booked_venues
		booked_venues = booked_venues.filter(Q(status=Bookrequest.APPROVED))
		#print "Approved",booked_venues
		return queryset.filter(~Q(venueid__in=booked_venues.values('venueid')))

	class Meta:
		model = Venue
		fields = ['capacity','dno']




class inline_equip(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(inline_equip, self).__init__(*args, **kwargs)
		# Filter queryset fields to groups
		self.fields['etypeid'].queryset = Equipment.objects.filter(etypeid__gte=0)

		class Meta:
			model = Equipment





class Resform(forms.ModelForm):

	class Meta:
		model = Equipment
		fields = ['etypeid','ename']

	def __init__(self,*args,**kwargs):
		super(Resform, self).__init__(*args, **kwargs)
		self.fields['etypeid'].disabled = True
		self.fields['ename'].required = True
		id = Equipment.objects.order_by('etypeid')
		if id:
			self.fields['etypeid'].initial = id[0].etypeid - 1
		else:
			self.fields['etypeid'].initial = -1

