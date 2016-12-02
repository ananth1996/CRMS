from django import forms
from .models import Resourcereq,FacultyRequest,Equipment,Student,Faculty


class EquipReqForm(forms.ModelForm):
	class Meta:
		model = Resourcereq
		fields = ['reqid','etypeid']

	def __init__(self,*args,**kwargs):
		#venue_id = kwargs.pop('venue_id',None)
		super(EquipReqForm, self).__init__(*args, **kwargs)
		#self.fields['venueid'].queryset = Venue.objects.filter(dno=Venue.objects.get(pk=venue_id).dno)
		self.fields['reqid'].label = "Equipment Booking ID"
		reqid=Resourcereq.objects.order_by('-reqid')


		if reqid:
			self.fields['reqid'].initial = reqid[0].reqid +1
		else:
			self.fields['reqid'].initial = 0

		self.fields['reqid'].disabled =True

		self.fields['etypeid'].required = True
		self.fields['etypeid'].queryset = Equipment.objects.filter(etypeid__lt=0)



class editReqForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(editReqForm, self).__init__(*args, **kwargs)
		self.fields['status'].required = True

	class Meta:
		model = Resourcereq
		fields = ['status']
