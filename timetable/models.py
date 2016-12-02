from django.db import models
from log.models import Faculty
from rooms.models import Venue
# Create your models here.


class Course(models.Model):
    idcourse = models.IntegerField(db_column='idCourse', primary_key=True)  # Field name made lowercase.
    cname = models.CharField(db_column='CName', max_length=45, blank=True)  # Field name made lowercase.
    weekhours = models.IntegerField(db_column='Weekhours', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'course'



class Timeslot(models.Model):
	timeslot_field = models.IntegerField(db_column='Timeslot#')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
	dayofweek = models.IntegerField(db_column='Dayofweek')  # Field name made lowercase.
	facultyid = models.ForeignKey(Faculty, db_column='FacultyID', blank=True, null=True)  # Field name made lowercase.
	courseid = models.ForeignKey(Course, db_column='CourseID', blank=True, null=True)  # Field name made lowercase.
	venueid = models.ForeignKey('Venue', db_column='VenueID', blank=True, null=True)  # Field name made lowercase.
	type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = True
		db_table = 'timeslot'

