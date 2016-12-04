from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from faults.forms import addFaultForm, editFaultForm
from log.models import UserProfile

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from rooms.models import Venue, VenueEquipment, Equipment
from faults.models import Fault
from log.views import isAdmin
from django.forms import inlineformset_factory


# Create your views here.


class addFault(LoginRequiredMixin, TemplateView):
	login_url = '/log/login/'

	def get(self, request):
		form = addFaultForm()
		return render(request, 'faults/addFault.html', {'form': form})

	def post(self, request):
		form = addFaultForm(data=request.POST)

		if form.is_valid():
			fault = form.save(commit=False)
			qs = VenueEquipment.objects.filter(etypeid=fault.etype)
			cross_check = qs.values_list('venueid',flat=True)
			if fault.venueid_id in cross_check:
				venueequip =qs.get(venueid=fault.venueid_id)
				if venueequip.quantity >0:
					#redudce equipment quantity
					venueequip.quantity -=1
					venueequip.save()
					fault.status=Fault.Pen
					fault.save()
					messages.success(request,"Fault Was Added Successfully")
					return HttpResponseRedirect('/home')
				else:
					form.add_error('etype',"Cannot add fault to "+str(fault.etype)+" as qauntity of items present in venue is 0")
			else:
				form.add_error('etype',"Equipment "+str(fault.etype)+" is not present in venue "+str(fault.venueid))

		return render(request, 'faults/addFault.html', {'form': form})


@login_required(login_url='/log/login/')
def viewFault(request):
	fault_obj = Fault.objects.all()
	equip_obj = Equipment.objects.all()
	return render(request, 'faults/viewFaults.html', {'fault_obj': fault_obj, 'equip_obj': equip_obj})


class editFault(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
	login_url = '/log/login/'

	def test_func(self):
		if not isAdmin(self.request.user):
			messages.error(self.request," Profile {0} Does Not Have The Priviliges to Access This Site. Please Log in with a Valid Profile to Proceed ".format(self.request.user))
		return isAdmin(self.request.user)

	def get(self, request, fault_id):
		fault = Fault.objects.get(pk=fault_id)
		editform = editFaultForm(initial={'status':fault.status})
		return render(request, 'faults/editFaults.html', {'editform': editform, 'fault': fault})

	def post(self,request,fault_id):
		fault = Fault.objects.get(pk = fault_id)
		if 'delete' in request.POST:
			fault.delete()
			messages.success(request,'Fault was deleted sucessfully',)
			return HttpResponseRedirect('/home')

		form = editFaultForm(request.POST,instance=fault)

		if form.is_valid():
			obj=form.save(commit=False)
			if obj.status == Fault.Done:
				qs = VenueEquipment.objects.get(venueid=obj.venueid, etypeid=obj.etype)
				qs.quantity += 1
				qs.save()

			messages.success(request,'Fault was edited successfully')
			return HttpResponseRedirect('/home')


		return render(request, 'faults/editFaults.html', {'editform': form, 'fault': fault})




