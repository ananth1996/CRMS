from django.contrib import admin
from rooms.models import Venue,VenueEquipment,Equipment,Bookrequest,FacultyBook,StudentBook
# Register your models here.

class VenueAdmin(admin.ModelAdmin):

	list_display = ('venuename','dno','capacity')
	list_filter = ['dno']

class VenueEquipAdmin(admin.ModelAdmin):
	list_display = ['venueid','etypeid','quantity']

class BookAdmin(admin.ModelAdmin):
	list_display = ['idbookrequest','venueid','starttime','endtime','status',]



class FacultyBookAdmin(admin.ModelAdmin):
	list_display = ['bookid','facultyid','get_booking_status','get_booking_venue']
	def get_booking_status(self,obj):
		return obj.bookid.status
	get_booking_status.short_description = "Booking Status"
	def get_booking_venue(self,obj):
		return obj.bookid.venueid
	get_booking_venue.short_description = "Booking Venue"

class StudentBookAdmin(admin.ModelAdmin):
	list_display = ['bookid','usn','get_booking_status','get_booking_venue']
	def get_booking_status(self,obj):
		return obj.bookid.status
	get_booking_status.short_description = "Booking Status"

	def get_booking_venue(self,obj):
		return obj.bookid.venueid
	get_booking_venue.short_description = "Booking Venue"

admin.site.register(Venue,VenueAdmin)
admin.site.register(Equipment)
admin.site.register(VenueEquipment,VenueEquipAdmin)
admin.site.register(FacultyBook,FacultyBookAdmin)
admin.site.register(Bookrequest,BookAdmin)
admin.site.register(StudentBook,StudentBookAdmin)


# Register your models here.
