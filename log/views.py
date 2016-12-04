from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from forms import LoginForm,addStudForm,addFacForm,addPerForm
from django.views.generic  import TemplateView
from .models import Student,UserProfile
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.


def User_login(request):
	context =RequestContext(request)
	error =False
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			return HttpResponseRedirect('/home/')
		else:
			error=True
			return render(request, 'log/login.html',{'form': LoginForm(),'error': error})

	else:
		return render(request, 'log/login.html',{'form': LoginForm(),'error': error})


class User_logout(LoginRequiredMixin,TemplateView):
	login_url = '/log/login'

	def get(self, request, *args, **kwargs):
		logout(request)
		return HttpResponseRedirect('/')


class addStud(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
	login_url = '/log/login/'

	def test_func(self):
		if not isAdmin(self.request.user):
			messages.error(self.request," Profile {0} Does Not Have The Priviliges to access this site. Please log in with a valid Profile".format(self.request.user))
		return isAdmin(self.request.user)


	def get(self, request, *args, **kwargs):
		form = addStudForm()
		return render(request,'log/addStud.html',{'form':form})

	def post(self,request):
		form = addStudForm(data=request.POST)
		if form.is_valid():
			stud = form.save(commit=False)
			print stud.usn
			passw = request.POST['password']
			print passw
			try:
				user =User.objects.create_user(username=stud.usn,password=passw)
				print "here"
				stud.save()
				UserProfile.objects.create(user=user, student=stud, userType='S', priorityLevel=2)
				messages.success(request,"Sucessfully Added Student {0}".format(user))
				return HttpResponseRedirect('/home')
			except Exception as e :

				form.add_error('usn',e.args[1])

		return render(request, 'log/addStud.html', {'form': form})

class addFac(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
	login_url = '/log/login/'

	def test_func(self):
		if not isAdmin(self.request.user):
			messages.error(self.request," Profile {0} Does Not Have The Priviliges to Access This Site. Please Log in with a Valid Profile to Proceed ".format(self.request.user))
		return isAdmin(self.request.user)

	def get(self, request, *args, **kwargs):
		form = addFacForm()
		return render(request,'log/addFac.html',{'form':form})

	def post(self,request):
		form = addFacForm(data=request.POST)
		if form.is_valid():
			faculty = form.save(commit=False)
			#print faculty.usn
			passw = request.POST['password']
			#print passw
			try:
				user =User.objects.create_user(username=faculty.facultyid,password=passw)
				print "here"
				faculty.save()
				UserProfile.objects.create(user=user,faculty=faculty,userType='F',priorityLevel=1)
				messages.success(request,"Sucessfully Added Faculty {0}".format(user))
				return HttpResponseRedirect('/home')
			except Exception as e:

				form.add_error('facultyid',e.args[1])

		return render(request, 'log/addFac.html', {'form': form})


def isAdmin(user):
	return user.userprofile.userType == 'SA'


class addPer(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
	login_url = '/log/login/'

	def test_func(self):
		if not isAdmin(self.request.user):
			messages.error(self.request," Profile {0} Does Not Have The Priviliges to Access This Site. Please Log in with a Valid Profile to Proceed ".format(self.request.user))
		return isAdmin(self.request.user)

	def get(self, request, *args, **kwargs):
		form = addPerForm()
		return render(request,'log/addPer.html',{'form':form})

	def post(self,request):
		form = addPerForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		if form.is_valid():
			try:
				user =User.objects.create_user(username=username,password=password)
				UserProfile.objects.create(user=user,userType='P',priorityLevel=0)
				messages.success(request,"Sucessfully Added Personnel {0}".format(user))
				return HttpResponseRedirect('/home')
			except :
				form.add_error('username',"Username Already Exists")
				print form

		return render(request, 'log/addPer.html', {'form': form})





