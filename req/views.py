from django.shortcuts import render
from django.views.generic import TemplateView,FormView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from log.views import isAdmin
from django.contrib import messages
from .forms import EquipReqForm,editReqForm
from .models import Resourcereq,FacultyRequest,StudentRequest,Equipment
from django.http import HttpResponseRedirect
# Create your views here.



class addEquipReq(LoginRequiredMixin,TemplateView):
	login_url = '/log/login/'


	def get(self, request, *args, **kwargs):
		form = EquipReqForm()

		return render(request,'req/addReq.html',{'form':form })

	def post(self,request):
		form = EquipReqForm(data=request.POST)
		profile = request.user.userprofile
		if form.is_valid():
			equipreq = form.save(commit=False)
			equipreq.status = Resourcereq.PENDING
			if profile.userType == 'S':
				a = StudentRequest.objects.filter(reqid__etypeid = equipreq.etypeid,usn=profile.student)
				print a
			if profile.userType == 'F':
				a = FacultyRequest.objects.filter(reqid__etypeid= equipreq.etypeid,facultyid=profile.faculty)
				print a
			if not a :
				equipreq.save()
				if  profile.userType == 'F':
					FacultyRequest.objects.create(facultyid=profile.faculty,reqid=equipreq)
				elif  profile.userType == 'S':
					StudentRequest.objects.create(usn=profile.student,reqid=equipreq)
				messages.success(request,'Resource Request Successfully made')
				return HttpResponseRedirect('/home')

			else:
				form.add_error('etypeid',"Sorry You Have Already Made a Request for this Resource")

		return render(request,'req/addReq.html',{'form':form})



@login_required(login_url='/log/login/')
def viewReq(request):
	fault_obj = Resourcereq.objects.all()
	equip_obj = Equipment.objects.filter(etypeid__lt=0)
	return render(request, 'req/viewReq.html', {'fault_obj': fault_obj, 'equip_obj': equip_obj})


class editReq(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
	login_url = '/log/login/'

	def test_func(self):
		if not isAdmin(self.request.user):
			messages.error(self.request," Profile {0} Does Not Have The Priviliges to Access This Site. Please Log in with a Valid Profile to Proceed ".format(self.request.user))
		return isAdmin(self.request.user)

	def get(self, request, req_id):
		req = Resourcereq.objects.get(pk=req_id)
		editform = editReqForm(initial={'status':req.status})
		return render(request, 'req/editReq.html', {'editform': editform, 'fault': req})

	def post(self,request,req_id):
		req = Resourcereq.objects.get(pk = req_id)
		if 'delete' in request.POST:
			req.delete()
			messages.success(request,'Request was deleted sucessfully')
			return HttpResponseRedirect('/home')

		form = editReqForm(request.POST,instance=req)

		if form.is_valid():
			obj=form.save(commit=False)
			obj.save()
			messages.success(request,'Request was edited successfully')
			return HttpResponseRedirect('/home')


		return render(request, 'req/editReq.html', {'editform': form, 'fault': req})