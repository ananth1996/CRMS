from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import  TemplateView,ListView
from rooms.forms import  venueForm,editForm,equipForm, addDeptFor,bookVenueForm,VenueFilter,inline_equip,Resform
from log.views import isAdmin
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Venue,VenueEquipment,Equipment,Bookrequest,FacultyBook,StudentBook
from django.forms import inlineformset_factory
from django.contrib import messages
import datetime
from django.db.models import Q
import re
from django.template import RequestContext
# Create your views here.




class addVenue(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
	login_url = '/log/login/'


	def test_func(self):
		if not isAdmin(self.request.user):
			messages.warning(self.request," Profile {0} Does Not Have The Priviliges to access this site. Please log in with a valid Profile".format(self.request.user))
		return isAdmin(self.request.user)


	def get(self, request, *args, **kwargs):
		form = venueForm()

		return render(request,'rooms/addVenue.html',{'form':form })

	def post(self,request):
		form = venueForm(data=request.POST)
		if form.is_valid():
			venue = form.save()
			venue.save()
			messages.success(request,'Venue was Added Successfully')
			return HttpResponseRedirect('/home')



		return render(request,'rooms/addVenue.html',{'form':form})




class viewVenue(LoginRequiredMixin,ListView):
	login_url = '/log/login/'
	model = Venue
	template_name = 'rooms/viewVenue.html'


class editVenue(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
	login_url = '/log/login/'

	def test_func(self):
		if not isAdmin(self.request.user):
			messages.warning(self.request," Profile {0} Does Not Have The Priviliges to access this site. Please log in with a valid Profile".format(self.request.user))
		return isAdmin(self.request.user)


	def get(self,request,venue_id):
		venue_obj = Venue.objects.get(pk=venue_id)
		edit_form = editForm(initial={'venuename':venue_obj.venuename,'capacity':venue_obj.capacity})
		euipmentFormSet = inlineformset_factory(Venue, VenueEquipment,fields=('etypeid', 'quantity',),extra=1,max_num=len(Equipment.objects.filter(etypeid__gte=0)),form=inline_equip)

		formset = euipmentFormSet(instance = venue_obj)
		for forms in formset:
			for x in forms:
				print x.label,x.is_hidden,"\n\n",x
		return render(request,'rooms/editVenue.html',{'formset':formset,'venue':venue_obj,'edit_form':edit_form})

	def post(self,request,venue_id):
		form_class = editForm
		euipmentFormSet = inlineformset_factory(Venue, VenueEquipment, fk_name='venueid',fields=('etypeid', 'quantity',),extra=1,max_num=len(Equipment.objects.filter(etypeid__gte=0)),form=inline_equip)
		print "venue id",venue_id
		venue_obj = Venue.objects.get(pk=venue_id)
		if 'delete' in request.POST:
			venue_obj.delete()
			messages.success(request,'Venue was deleted sucessfully')
			return HttpResponseRedirect('/home')

		form =  form_class(request.POST,instance=venue_obj,initial={'venuename':venue_obj.venuename,'capacity':venue_obj.capacity})
		equipment_form = euipmentFormSet(request.POST,instance=venue_obj)

		if(form.is_valid() and equipment_form.is_valid()):
			form.save()
			print "done"
			equipment_form.save()
			return HttpResponseRedirect('/rooms/viewVenue')

		return render(request,'rooms/editVenue.html',{'formset':equipment_form,'venue':venue_obj,'edit_form':form})




class addEquip(LoginRequiredMixin,TemplateView):
	login_url = '/log/login/'
	def test_func(self):
		if not isAdmin(self.request.user):
			messages.warning(self.request," Profile {0} Does Not Have The Priviliges to access this site. Please log in with a valid Profile".format(self.request.user))
		return isAdmin(self.request.user)


	def get(self, request, *args, **kwargs):
		form = equipForm()

		return render(request,'rooms/addEquip.html',{'form':form })

	def post(self,request):
		form = equipForm(data=request.POST)
		if form.is_valid():
			equip = form.save()
			equip.save()
			messages.success(request,'Equipment was Added Successfully')
			return HttpResponseRedirect('/home')
		else:
			print form.errors


		return render(request,'rooms/addEquip.html',{'form':form})

class addDept(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
	login_url = '/log/login/'
	def test_func(self):
		if not isAdmin(self.request.user):
			messages.warning(self.request," Profile {0} Does Not Have The Priviliges to access this site. Please log in with a valid Profile".format(self.request.user))
		return isAdmin(self.request.user)


	def get(self,request):
		form = addDeptFor()
		return render(request,'rooms/addDept.html',{'form':form})

	def post(self,request):
		form = addDeptFor(data=request.POST)
		if form.is_valid():
			dept = form.save()
			dept.save()
			messages.success(request,'Department was Added Successfully')
			return HttpResponseRedirect('/home')


		return render(request,'rooms/addDept.html',{'form':form})



def check_collision(SA,EA,SB,EB):
	return (SA<EB) and (EA>SB)

class bookVenue(LoginRequiredMixin,TemplateView):
	login_url = '/log/login/'

	def get(self, request,venue_id,startdate,enddate,*args, **kwargs):

		startdate = datetime.datetime.strptime(startdate,"%Y-%m-%d")
		enddate = datetime.datetime.strptime(enddate, "%Y-%m-%d")

		form = bookVenueForm(initial={'venueid':venue_id,'starttime':startdate,'endtime':enddate})

		return render(request,'rooms/makeBook.html',{'form':form})

	def post(self,request,venue_id,startdate,enddate,*args,**kwargs):
		form = bookVenueForm(data=request.POST)
		if form.is_valid():
			booking = form.save(commit=False)
			booking.status = Bookrequest.PENDING
			#handle the yes no buttton for preemptuon first
			#print request.POST
			if 'yes' in request.POST:
				print "Clicked Yes"
				preempt = StudentBook.objects.filter(bookid__venueid=booking.venueid,
														bookid__status=Bookrequest.APPROVED,
														bookid__starttime__lt=booking.endtime,
														bookid__endtime__gt=booking.starttime)[0]
				preempt.bookid.status= Bookrequest.PREEMPT
				preempt.bookid.save()
				booking.save()
				print request.user.userprofile.faculty
				FacultyBook.objects.create(bookid=booking, facultyid=request.user.userprofile.faculty)
				messages.success(request,"Booking Request Successfully Made after Pre-Empt")
				return HttpResponseRedirect('/home')
			if 'no' in request.POST:
				print "Clicked No"
				messages.info(request,"Did Not Preempt Booking request Not Made")
				return HttpResponseRedirect('/home')

			if booking.starttime<=booking.endtime:
				general_conflicts = FacultyBook.objects.filter(bookid__venueid=booking.venueid,
												bookid__status=Bookrequest.APPROVED,
												bookid__starttime__lt=booking.endtime,
												bookid__endtime__gt=booking.starttime)

				#print qs
				if not general_conflicts :
					profile = request.user.userprofile
					#print profile
					collisions = StudentBook.objects.filter(bookid__venueid=booking.venueid,
															bookid__status=Bookrequest.APPROVED,
															bookid__starttime__lt=booking.endtime,
															bookid__endtime__gt=booking.starttime)
					#print collisions
					#If no student collisions also then make request
					if not collisions:
						booking.save()
						if profile.userType == 'F':
							FacultyBook.objects.create(bookid=booking,facultyid=profile.faculty)
						elif profile.userType =='S':
							StudentBook.objects.create(bookid=booking,usn=profile.student)

						messages.success(request,"Booking Request Was Succesfully Made")
						return HttpResponseRedirect('/home')
					#If Faculty or Admin give preemption warning if student collisons
					elif profile.userType == 'SA' or profile.userType == 'F':
							preempt = collisions[0]
							return render(request, 'rooms/makeBook.html', {'form': form, 'collision': preempt})
					#If student
					else:
						form.add_error(None,"Cannot Make Request Conflicting Booking Existing ")
				#If anyone gets conflicting bookings
				else:
					form.add_error(None, "Cannot Make Request Conflicting Booking Existing ")

			#If incorrect date time input
			else:
				form.add_error('endtime', "End date or end time  before start date or start time ")


		return render(request,'rooms/makeBook.html',{'form':form})




def venue_list(request):
	f = VenueFilter(request.GET, queryset=Venue.objects.all())
	data = f.data
	today = datetime.date.today().__str__()
	if data:
		if 'startdate' in data and 'enddate' in data :
			print "YES"
			if data['startdate']>data['enddate']:
				messages.error(request,"Start Date After End Date")
				return render(request, 'rooms/test.html', {'filter': f, 'now':today})


	val=[]
	#print f.qs

	for x in f.qs:

		e=VenueEquipment.objects.filter(venueid=x.venueid)
		val.append(e)

	details = zip(f.qs,val)

	return render(request, 'rooms/test.html', {'filter': f,'details':details, 'now':today})

class appovalView(LoginRequiredMixin,UserPassesTestMixin,ListView):
	login_url = '/log/login/'

	def test_func(self):
		if not isAdmin(self.request.user):
			messages.warning(self.request," Profile {0} Does Not Have The Priviliges to access this site. Please log in with a valid Profile".format(self.request.user))
		return isAdmin(self.request.user)

	template_name = 'rooms/approvalView.html'

	def get_queryset(self):
		queryset = Venue.objects.filter(bookrequest__status=Bookrequest.PENDING).distinct()
		val = []
		for v in queryset:
			c = v.bookrequest_set.all().filter(status=Bookrequest.PENDING).count()
			val.append(c)
		queryset = zip(queryset,val)
		return queryset

	def random(self, request, *args, **kwargs):
		invalid = Bookrequest.objects.filter(status=Bookrequest.PENDING,
											 starttime__lt=dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		if invalid:
			for i in invalid:
				i.status = Bookrequest.DENIED
				i.save()

		pending = Bookrequest.objects.filter(status=Bookrequest.PENDING)
		venues = Venue.objects.filter(bookrequest__status=Bookrequest.PENDING).distinct()
		print venues
		print pending
		for v in venues:
			print "For venue",v
			b = v.bookrequest_set.all().filter(status=Bookrequest.PENDING)
			for i in b:
				coll = b.filter(~Q(idbookrequest=i.idbookrequest),starttime__lt=i.endtime,endtime__gt=i.starttime)
				print "collisions of ",i," with ",coll




class approvalVenue(LoginRequiredMixin,UserPassesTestMixin,ListView):
	login_url = '/log/login/'

	def test_func(self):
		if not isAdmin(self.request.user):
			messages.warning(self.request," Profile {0} Does Not Have The Priviliges to access this site. Please log in with a valid Profile".format(self.request.user))
		return isAdmin(self.request.user)

	template_name = 'rooms/approvalVenue.html'

	def get_context_data(self, **kwargs):
		context = super(approvalVenue, self).get_context_data(**kwargs)
		context['venue'] = Venue.objects.get(venueid=self.kwargs['venue_id'])
		return context

	def get_queryset(self,*args,**kwargs):
		id = self.kwargs['venue_id']
		v = Venue.objects.get(venueid=id)
		queryset = v.bookrequest_set.all().filter(status=Bookrequest.PENDING)
		print "pending query set",queryset
		val =[]
		consider = []
		for x in queryset:
			consider.append(x)

		for x in queryset[:]:
			if(x in consider):
				coll = queryset.filter(starttime__lt=x.endtime, endtime__gt=x.starttime)

				for i in coll:
					try:
						consider.remove(i)
					except:
						pass
				if not coll:
					coll=queryset.filter(idbookrequest=x.idbookrequest)
					print x
					print "NO SELF IN COLLISIONS",x,coll
				val.append(coll)

		return val

	def get(self, request, *args, **kwargs):
		print self.request.GET
		invalid = Bookrequest.objects.filter(status=Bookrequest.PENDING,
											 starttime__lt=dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		if invalid:
			for i in invalid:
				i.status = Bookrequest.DENIED
				i.save()

		qs =self.get_queryset(*args,**kwargs)
		#print qs
		if 'Approve' in self.request.GET:
			print "YES"
			val = request.GET['Approve']
			reg = re.compile(r'(?P<click>\d+)$')
			click = reg.search(val).group('click')
			app = Bookrequest.objects.get(pk=click)
			for x in qs:
				if app in x :
					for i in x:
						if i == app:
							app.status=Bookrequest.APPROVED
							app.save()
							print "Saving"
						else:
							i.status=Bookrequest.DENIED
							i.save()
							print "Saving"





		return super(approvalVenue, self).get(request, *args, **kwargs)




class addRes(LoginRequiredMixin,TemplateView):
	login_url = '/log/login/'
	def test_func(self):
		if not isAdmin(self.request.user):
			messages.warning(self.request," Profile {0} Does Not Have The Priviliges to access this site. Please log in with a valid Profile".format(self.request.user))
		return isAdmin(self.request.user)


	def get(self, request, *args, **kwargs):
		form = Resform()

		return render(request,'rooms/addEquip.html',{'form':form })

	def post(self,request):
		form = Resform(data=request.POST)
		if form.is_valid():
			equip = form.save()
			equip.save()
			messages.success(request,'Resource was Added Successfully')
			return HttpResponseRedirect('/home')
		else:
			print form.errors


		return render(request,'rooms/addEquip.html',{'form':form})
