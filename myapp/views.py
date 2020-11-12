from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from datetime import datetime
from .models import *
import collections

def testserver(request):
	return HttpResponse("Sever has started successfully")

def index(request):

	participants = request.POST['useremails'].split(',')

	if isValidCount(list(participants)) == False:
		data = {
		"errormsg" : "Number of participants are less than 2"
		}
		return render(request,'index.html',context=data)

	
	allinterviewsjson = d
	del d

	data = {
		"allinterviews" : allinterviewjson
	}
	return render(request,'index.html',context=data)

def getallinterviewsapi(request):
	
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

	data = {
	"allinterviews" : allinterviewsdict
	}

	return JsonResponse(data) 

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

def onsubmit(request):

	
	
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
		key = Interview.objects.get(id=schedule.interview_id).title
		value = Participant.objects.get(id=schedule.participant_id).useremail
		d[key].append(value)

	data = {
		"d" : d
	}
	
	return JsonResponse(data)
	return render(request,'index.html',context=data)
	


def isValidCount(participants):
	if len(participants) < 2:
		return False
	else:
		return True

# Create your views here.
