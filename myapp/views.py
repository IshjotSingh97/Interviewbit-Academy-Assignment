from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from datetime import datetime
from .models import *
import collections

def testserver(request):
	return HttpResponse("Sever has started successfully")

def getallinterviews():
	
	d = collections.defaultdict(lambda : collections.defaultdict())

	for schedule in Schedule.objects.all():
		interview = Interview.objects.get(id=schedule.interview_id)
		title = interview.title
		starttime = interview.starttime
		endtime = interview.endtime
		d[title]["starttime"] = starttime
		d[title]["endtime"] = endtime
		d[title]["participants"] = []
		
	for schedule in Schedule.objects.all():
		interview = Interview.objects.get(id=schedule.interview_id)
		participant = Participant.objects.get(id=schedule.participant_id)
		d[interview.title]["participants"].append(participant.useremail)

	allinterviewsdict = d
	del d

	return allinterviewsdict

def getallinterviewsapi(request):
	
	allinterviews = getallinterviews()
	
	data = {
		"allinterviews" : allinterviews
	}

	return JsonResponse(data) 


def index(request):

	allinterviews = getallinterviews()
	
	data = {
		"allinterviews" : allinterviews
	}

	return render(request,'index.html',context=data)


def onsubmit(request):

	participants = request.POST['useremails'].split(',')

	if isValidCount(list(participants)) == False:
		data = {
		"errormsg" : "Number of participants are less than 2"
		}
		return render(request,'index.html',context=data)
	
	elif isValidSchedule(list(participants)) == False:
		data = {
		"errormsg" : "Confict of schedule"
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

	

	successmsg = "Interview scheduled successfully"
	
	data = {
		"allinterviews" : allinterviews,
		"successmsg" : successmsg
	}

	allinterviews = getallinterviews()

	
	return JsonResponse(data)
	return render(request,'index.html',context=data)
	


def isValidCount(participants):
	if len(participants) < 2:
		return False
	else:
		return True

# Create your views here.
