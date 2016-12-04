from django.db import models
from rooms.models import  Venue,Equipment,VenueEquipment
from django.db.models.signals import pre_delete
from django.dispatch import receiver
# Create your models here.



class Fault(models.Model):
	Pen = "Pending"
	Repair = "Repairing"
	Done = "Completed"

	STATUS_OPTIONS = (
		(Pen, "Pending Repair"),
		(Repair, "Getting Repaired"),
		(Done, "Completed Repair"),
	)

	idfault = models.IntegerField(db_column='idFault', primary_key=True)  # Field name made lowercase.
	venueid = models.ForeignKey(Venue, models.CASCADE, db_column='VenueID', blank=True, null=True)  # Field name made lowercase.
	etype = models.ForeignKey(Equipment, models.CASCADE, db_column='etype', blank=True, null=True)
	status = models.CharField(db_column='Status', max_length=45, blank=True, null=True,choices=STATUS_OPTIONS,default=Pen)  # Field name made lowercase.

	class Meta:
		managed = True
		db_table = 'fault'

	def __unicode__(self):
		return "Fault {0}".format(self.idfault)


#before deleting the fault increment the equipment value in the veneu
@receiver(pre_delete, sender=Fault)
def post_delete_user(sender, instance, *args, **kwargs):
	if instance.status != Fault.Done:
		qs = VenueEquipment.objects.get(venueid=instance.venueid,etypeid=instance.etype)
		qs.quantity+=1
		qs.save()
