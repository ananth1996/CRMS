from django.db import models
from log.models import Student, Faculty
from rooms.models import Venue,Equipment

# Create your models here.



class Resourcereq(models.Model):
	PENDING = "Pending Approval"
	DENIED = "Denied Approval"
	APPROVED = "APPROVED"
	CHOICES = (
		(PENDING, PENDING),
		(DENIED, DENIED),
		(APPROVED, APPROVED),
	)
	reqid = models.IntegerField(db_column='ReqID', primary_key=True)  # Field name made lowercase.
	etypeid = models.ForeignKey(Equipment, models.CASCADE, db_column='EtypeID', blank=True, null=True)  # Field name made lowercase.
	venueid = models.ForeignKey(Venue, models.CASCADE, db_column='VenueID', blank=True, null=True)  # Field name made lowercase.
	status = models.CharField(db_column='Status', max_length=45, blank=True, null=True,choices=CHOICES)  # Field name made lowercase.

	class Meta:
		managed = True
		db_table = 'resourcereq'

	def __unicode__(self):
		return "Resource Request {0} for {1}".format(self.reqid,self.etypeid)





class StudentRequest(models.Model):
	usn = models.ForeignKey(Student, models.CASCADE, db_column='USN')  # Field name made lowercase.
	reqid = models.ForeignKey(Resourcereq, models.CASCADE, db_column='ReqID')  # Field name made lowercase.

	class Meta:
		managed = True
		db_table = 'student_request'
		unique_together = (('usn', 'reqid'),)

	def __unicode__(self):
		return "{0} Request for Resource: {1}".format(self.usn,self.reqid.etypeid)


class FacultyRequest(models.Model):
	facultyid = models.ForeignKey(Faculty, models.CASCADE, db_column='FacultyID')  # Field name made lowercase.
	reqid = models.ForeignKey('Resourcereq', models.CASCADE, db_column='ReqID')  # Field name made lowercase.

	class Meta:
		managed = True
		db_table = 'faculty_request'
		unique_together = (('facultyid', 'reqid'),)

	def __unicode__(self):
		return "{0} Request for Resource: {1}".format(self.facultyid,self.reqid.etypeid)


