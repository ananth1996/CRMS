from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from log.views import isAdmin
from django.views.generic import ListView,TemplateView
from rooms.models import FacultyBook,StudentBook,Bookrequest
from req.models import FacultyRequest,StudentRequest,Resourcereq
from faults.models import Fault
from django.http import HttpResponseRedirect
import datetime
from django.contrib import messages
from django.db.models import Q
from forms import PrintForm
from django.utils import timezone

#@user_passes_test(isAdmin,login_url='/log/login/')

import datetime as dt
class Home(LoginRequiredMixin,TemplateView):
	login_url = '/log/login/'
	template_name = 'home.html'

	def get(self, request, *args, **kwargs):
		#form = PrintForm(initial={'starttime':datetime.datetime.now().date(),'endtime':datetime.datetime.now().date()})
		form = PrintForm()
		profile = request.user.userprofile
		booking = {}
		requests = {}
		invalid = Bookrequest.objects.filter(status=Bookrequest.PENDING, starttime__lt=dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		if invalid:
			for i in invalid:
				i.status = Bookrequest.DENIED
				i.save()

		pendingBook = len(Bookrequest.objects.filter(status=Bookrequest.PENDING))
		pendingFault = len(Fault.objects.filter(~Q(status=Fault.Done)))
		pendingReq = len(Resourcereq.objects.filter(status=Resourcereq.PENDING))
		badges = {'pending':pendingBook,'faults':pendingFault,'req':pendingReq}

		if profile.userType == 'F' :
			booking = Bookrequest.objects.filter(facultybook__facultyid=profile.faculty)
			requests = Resourcereq.objects.filter(facultyrequest__facultyid=profile.faculty)
		elif profile.userType == 'S':
			booking = Bookrequest.objects.filter(studentbook__usn=profile.student)
			requests = Resourcereq.objects.filter(studentrequest__usn=profile.student)
		if len(booking):
			k = []
			for b in booking:
				if b.endtime < timezone.now():
					k.append(False)
					continue
				if b.status == Bookrequest.PENDING or b.status== Bookrequest.APPROVED:
					k.append(True)
				else:
					k.append(False)
		cancellable = zip(booking,k)
		return render(request,'home.html',{'booking':booking,'requests':requests,'form':form,'badges':badges,'cancellable':cancellable})

	def post(self,request):
		starttime = request.POST['starttime']
		endtime = request.POST['endtime']
		form = PrintForm(data=request.POST)
		profile = request.user.userprofile
		booking = {}
		requests = {}
		pendingBook = len(Bookrequest.objects.filter(status=Bookrequest.PENDING))
		pendingFault = len(Fault.objects.filter(~Q(status=Fault.Done)))
		pendingReq = len(Resourcereq.objects.filter(status=Resourcereq.PENDING))
		badges = {'pending':pendingBook,'faults':pendingFault,'req':pendingReq}

		if profile.userType == 'F' :
			booking = Bookrequest.objects.filter(facultybook__facultyid=profile.faculty)
			requests = Resourcereq.objects.filter(facultyrequest__facultyid=profile.faculty)
		elif profile.userType == 'S':
			booking = Bookrequest.objects.filter(studentbook__usn=profile.student)
			requests = Resourcereq.objects.filter(studentrequest__usn=profile.student)

		if starttime>endtime:
			messages.error(request,"Invalid Date Range")
			return HttpResponseRedirect('/home')
		if starttime and endtime and form.is_valid():
			url = '/print/schedule/'+starttime.__str__()+'/'+endtime.__str__()
			return HttpResponseRedirect(url)
		elif not starttime:
			messages.warning(request,"Schedule Needs a Valid StartDate")
		elif not endtime:
			messages.warning(request,"Schedule Needs Valid EndTime")
		return HttpResponseRedirect('/home')





def slash(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/home')

	return  render(request,'index.html')


def printBook(request,bookid):
	book = Bookrequest.objects.get(pk=bookid)
	return render(request,'printApproval.html',{'book':book})


def printreq(request,reqid):
	req = Resourcereq.objects.get(pk=reqid)
	return render(request,'printApprovalR.html',{'req':req})

def printFault(request):
	f = Fault.objects.filter(~Q(status=Fault.Done))
	print f
	return render(request,'printFaults.html',{'faults':f})
	

def printSchedule(request,start,end):
	#start = datetime.datetime.strptime(start, "%Y-%m-%d")
	#end = datetime.datetime.strptime(end, "%Y-%m-%d")
	e = Bookrequest.objects.filter(status=Bookrequest.APPROVED,starttime__gte=start,endtime__lte=end)
	print e
	return render(request,'printEventSchedule.html',{'events':e,'startdate':start,'enddate':end})


def cancelBook(request,bookid):
	book = Bookrequest.objects.get(pk=bookid)
	old_stat = book.status
	book.status = Bookrequest.CANCELLED
	book.save()
	if old_stat == Bookrequest.APPROVED:
		collisions = Bookrequest.objects.filter(venueid=book.venueid,status=Bookrequest.DENIED,starttime__lte=book.endtime,endtime__gte=book.starttime)

		for coll in collisions:
			print coll
			coll.status=Bookrequest.PENDING
			coll.save()


	messages.success(request,"Succesfully Cancelled Booking ")
	return HttpResponseRedirect('/home')



