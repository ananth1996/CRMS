from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete
# Create your models here.

class Department(models.Model):
	dno = models.IntegerField(db_column='DNo', primary_key=True)  # Field name made lowercase.
	dname = models.CharField(db_column='DName', max_length=45, blank=True)  # Field name made lowercase.

	class Meta:
		managed = True
		db_table = 'department'

	def __unicode__(self):
		return self.dname

class Student(models.Model):
	usn = models.CharField(db_column='USN', primary_key=True, max_length=12)  # Field name made lowercase.
	name = models.CharField(db_column='Name', max_length=45, blank=True)  # Field name made lowercase.
	dno = models.ForeignKey(Department, db_column='DNo', blank=True, null=True)  # Field name made lowercase.
	
	class Meta:
		managed = True
		db_table = 'student'

	def __unicode__(self):
		return self.name

class Faculty(models.Model):
	facultyid = models.CharField(db_column='FacultyID', primary_key=True, max_length =6)
	name = models.CharField(db_column='Name',max_length=45,blank=True)
	dno = models.ForeignKey(Department, db_column='DNo', blank=True, null= True)

	class Meta:
		managed = True
		db_table = 'faculty'

	def __unicode__(self):
		return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	User_Type_Choices = (
			('SA','SysAdmin'),
			('S' ,'Student'),
			('F' ,'Faculty'),
			('P' ,'Personnel'),
			)
	userType = models.CharField(max_length=10,choices=User_Type_Choices,default='SA')
	priorityLevel = models.IntegerField(default=0)
	student = models.OneToOneField(Student,null=True,blank=True)
	faculty = models.OneToOneField(Faculty,null=True,blank=True)

	def __unicode__(self):
		return self.user.username


@receiver(post_delete,sender = UserProfile)
def post_delete_user(sender,instance,*args,**kwargs):
		instance.user.delete()



