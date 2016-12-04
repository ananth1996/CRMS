from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from log.models import Department,Student,Faculty



class Venue(models.Model):
	venueid = models.IntegerField(db_column='VenueID', primary_key=True)  # Field name made lowercase.
	venuename = models.CharField(db_column='VenueName', max_length=45, blank=True, null=True)  # Field name made lowercase.
	dno = models.ForeignKey(Department, models.CASCADE, db_column='DNo', blank=True, null=True)  # Field name made lowercase.
	capacity = models.IntegerField(db_column='Capacity', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed =True
		db_table = 'venue'

	def __unicode__(self):
		return self.venuename


class Equipment(models.Model):
	etypeid = models.IntegerField(db_column='EtypeID', primary_key=True)  # Field name made lowercase.
	ename = models.CharField(db_column='EName', max_length=45, blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = True
		db_table = 'equipment'

	def __unicode__(self):
		return self.ename


class VenueEquipment(models.Model):
	venueid = models.ForeignKey(Venue, models.CASCADE, db_column='VenueID')  # Field name made lowercase.
	etypeid = models.ForeignKey(Equipment, models.CASCADE, db_column='EtypeID')  # Field name made lowercase.
	quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = True
		db_table = 'venue_equipment'
		unique_together = (('venueid', 'etypeid'),)

	def __unicode__(self):
		return '{0} , {1}'.format(self.venueid,self.etypeid)


class Bookrequest(models.Model):
	PENDING = "Pending Approval"
	DENIED  = "Denied Approval"
	APPROVED = "APPROVED"
	PREEMPT = "Prempted by Staff"
	CANCELLED ='Cancelled'
	CHOICES = (
		(PENDING,PENDING),
		(DENIED,DENIED),
		(APPROVED,APPROVED),
		(PREEMPT, PREEMPT),
		(CANCELLED,CANCELLED),
	)
	idbookrequest = models.IntegerField(db_column='idBookRequest', primary_key=True)  # Field name made lowercase.
	venueid = models.ForeignKey('Venue', models.DO_NOTHING, db_column='VenueID', blank=True, null=True)  # Field name made lowercase.
	starttime = models.DateTimeField(db_column='StartTime', blank=True, null=True)  # Field name made lowercase.
	endtime = models.DateTimeField(db_column='EndTime', blank=True, null=True)  # Field name made lowercase.
	status = models.CharField(max_length=45, blank=True,choices=CHOICES, null=True,default=PENDING)

	class Meta:
		managed = True
		db_table = 'bookrequest'

	def __unicode__(self):
		return 'Booking No {0}'.format(self.idbookrequest)


class StudentBook(models.Model):
	usn = models.ForeignKey(Student,on_delete=models.CASCADE, db_column='USN')  # Field name made lowercase.
	bookid = models.ForeignKey(Bookrequest, db_column='idBookRequest',on_delete=models.CASCADE)  # Field name made lowercase.

	class Meta:
		managed = True
		db_table = 'student_book'
		unique_together = (('usn', 'bookid'),)

	def __unicode__(self):
		return 'Student Booking ID {0} {1}'.format(self.bookid_id,self.usn)


class FacultyBook(models.Model):
	facultyid = models.ForeignKey(Faculty,on_delete=models.CASCADE, db_column='FacultyID')  # Field name made lowercase.
	bookid = models.ForeignKey(Bookrequest,db_column='idBookRequest',on_delete=models.CASCADE)  # Field name made lowercase.

	class Meta:
		managed = True
		db_table = 'faculty_book'
		unique_together = (('facultyid', 'bookid'),)

	def __unicode__(self):
		return 'Faculty Booking {0} {1}'.format(self.bookid_id,self.facultyid)