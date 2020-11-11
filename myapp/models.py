from django.db import models

# Create your models here.
class Participant(models.Model):
	useremail = models.CharField(max_length=30)

class Interview(models.Model):
	title = models.CharField(max_length=30)
	starttime = DateTimeField()
	endtime = DateTimeField()

class Schedule(models.Model):
	participant = models.ForeignKey(Participant,on_delete=models.CASCADE)
	interview = models.ForeignKey(Interview,on_delete=models.CASCADE)