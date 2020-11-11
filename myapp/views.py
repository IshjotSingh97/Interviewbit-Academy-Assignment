from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from datetime import datetime
from .models import *
from collections import defaultdict

def testserver(request):
	return HttpResponse("Sever has started successfully")

def index(request):
	return render(request,'index.html')

def onsubmit(request):

	participants = request.POST['useremails'].split(',')

	if isValidCount(list(participants)) == False:
		data = {
		"errormsg" : "Number of participants are less than 2"
		}
		return render(request,'index.html',context=data)
	
	# logic for interview
	interview = Interview()
	interview.title = request.POST['title']
	interview.date = request.POST['date']
	interview.starttime = request.POST['starttime']
	interview.endtime = request.POST['endtime']
	interview.save()

	# logic for participants
	for i in range(len(participants)):
		participant = Participant()
		participant.useremail = participants[i]
		participant.save()

		# logic for schedule
		schedule = Schedule()
		schedule.participant_id = participant.id
		schedule.interview_id = interview.id
		schedule.save()

	d = collections.defaultdict(lambda : [])

	for schedule in Schedule.objects.all():
		key = Interview.objects.get(id=schedule.interview_id)
		value = Participant.objects.get(id=schedule.participant_id)
		d[key].append(value)

	data = {
		"d" : d
	}
	
	return render(request,'index.html',context=data)
	


def isValidCount(participants):
	if len(participants) < 2:
		return False
	else:
		return True

# Create your views here.
