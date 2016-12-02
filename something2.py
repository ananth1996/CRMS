# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Bookrequest(models.Model):
    idbookrequest = models.IntegerField(db_column='idBookRequest', primary_key=True)  # Field name made lowercase.
    venueid = models.ForeignKey('Venue', models.DO_NOTHING, db_column='VenueID', blank=True, null=True)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bookrequest'


class Course(models.Model):
    idcourse = models.IntegerField(db_column='idCourse', primary_key=True)  # Field name made lowercase.
    cname = models.CharField(db_column='CName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    weekhours = models.IntegerField(db_column='Weekhours', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'course'


class Department(models.Model):
    dno = models.IntegerField(db_column='DNo', primary_key=True)  # Field name made lowercase.
    dname = models.CharField(db_column='DName', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'department'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Equipment(models.Model):
    etypeid = models.IntegerField(db_column='EtypeID', primary_key=True)  # Field name made lowercase.
    ename = models.CharField(db_column='EName', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'equipment'


class Faculty(models.Model):
    facultyid = models.CharField(db_column='FacultyID', primary_key=True, max_length=6)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    dno = models.ForeignKey(Department, models.DO_NOTHING, db_column='DNo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'faculty'


class FacultyBook(models.Model):
    facultyid = models.ForeignKey(Faculty, models.DO_NOTHING, db_column='FacultyID')  # Field name made lowercase.
    bookid = models.ForeignKey(Bookrequest, models.DO_NOTHING, db_column='BookID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'faculty_book'
        unique_together = (('facultyid', 'bookid'),)


class FacultyRequest(models.Model):
    facultyid = models.ForeignKey(Faculty, models.DO_NOTHING, db_column='FacultyID')  # Field name made lowercase.
    reqid = models.ForeignKey('Resourcereq', models.DO_NOTHING, db_column='ReqID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'faculty_request'
        unique_together = (('facultyid', 'reqid'),)


class Fault(models.Model):
    idfault = models.IntegerField(db_column='idFault', primary_key=True)  # Field name made lowercase.
    venueid = models.ForeignKey('Venue', models.DO_NOTHING, db_column='VenueID', blank=True, null=True)  # Field name made lowercase.
    etype = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='etype', blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fault'


class Resourcereq(models.Model):
    reqid = models.IntegerField(db_column='ReqID', primary_key=True)  # Field name made lowercase.
    etypeid = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='EtypeID', blank=True, null=True)  # Field name made lowercase.
    venueid = models.ForeignKey('Venue', models.DO_NOTHING, db_column='VenueID', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'resourcereq'


class Student(models.Model):
    usn = models.CharField(db_column='USN', primary_key=True, max_length=12)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    dno = models.ForeignKey(Department, models.DO_NOTHING, db_column='DNo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'student'


class StudentBook(models.Model):
    usn = models.ForeignKey(Student, models.DO_NOTHING, db_column='USN')  # Field name made lowercase.
    bookid = models.ForeignKey(Bookrequest, models.DO_NOTHING, db_column='BookID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'student_book'
        unique_together = (('usn', 'bookid'),)


class StudentRequest(models.Model):
    usn = models.ForeignKey(Student, models.DO_NOTHING, db_column='USN')  # Field name made lowercase.
    reqid = models.ForeignKey(Resourcereq, models.DO_NOTHING, db_column='ReqID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'student_request'
        unique_together = (('usn', 'reqid'),)


class Venue(models.Model):
    venueid = models.IntegerField(db_column='VenueID', primary_key=True)  # Field name made lowercase.
    venuename = models.CharField(db_column='VenueName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    dno = models.ForeignKey(Department, models.DO_NOTHING, db_column='DNo', blank=True, null=True)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'venue'


class VenueEquipment(models.Model):
    venueid = models.ForeignKey(Venue, models.DO_NOTHING, db_column='VenueID')  # Field name made lowercase.
    etypeid = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='EtypeID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'venue_equipment'
        unique_together = (('venueid', 'etypeid'),)
