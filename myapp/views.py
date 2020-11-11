from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from datetime import datetime
from .models import *

def testserver(request):
	return HttpResponse("Sever has started successfully")

def index(request):
	return render(request,'index.html')

def onsubmit(request):
	# logic for participants
	participants = request.POST['useremails'].split(',')
	for i in range(len(participants)):
		participant = Participant()
		participant.useremail = participants[i]
		participant.save()
	# logic for interview
	interview = Interview()
	interview.title = request.POST['title']
	interview.date = request.POST['date']
	interview.starttime = request.POST['starttime']
	interview.endttime = request.POST['endtime']
	interview.save()
	return render(request,'index.html')
	

def isValidCount(participants):
	if len(participants) < 2:
		errormsg = "Number of participants are less than 2"
		return False
	else:
		validmsg = "This schedule is valid"
		return True

# Create your views here.
