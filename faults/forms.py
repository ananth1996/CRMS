from django import forms
from faults.models import Fault
from rooms.models import Equipment,VenueEquipment

class addFaultForm(forms.ModelForm):

	class Meta:
		model = Fault
		fields = ['idfault','venueid','etype',]

	def __init__(self, *args, **kwargs):
		venue_id = kwargs.pop('venue_id', None)
		super(addFaultForm, self).__init__(*args, **kwargs)
		self.fields['venueid'].required =True
		self.fields['etype'].required = True
		self.fields['etype'].label = "Equipment"
		self.fields['idfault'].label = "Fault ID"
		self.fields['etype'].queryset = Equipment.objects.filter(etypeid__gt=0)
		id = Fault.objects.order_by('-idfault')
		if id:
			self.fields['idfault'].initial = id[0].idfault + 1
		else:
			self.fields['idfault'].initial = 0

		self.fields['idfault'].disabled = True


class editFaultForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(editFaultForm, self).__init__(*args, **kwargs)
		self.fields['status'].required = True

	class Meta:
		model = Fault
		fields = ['status']
