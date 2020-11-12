from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from datetime import datetime
from .models import *
import collections

def testserver(request):
	return HttpResponse("Sever has started successfully")

def getallinterviews():
	
	jsonArr = []

	for schedule in Schedule.objects.all():
		d = {}
		d["participants"] = []
		interview = Interview.objects.get(id=schedule.interview_id)
		title = interview.title
		date = interview.date
		starttime = interview.starttime
		endtime = interview.endtime
		d["title"] = title
		d["date"] = date
		d["starttime"] = starttime
		d["endtime"] = endtime
		jsonArr.append(d)
		
	for schedule in Schedule.objects.all():
		interviewtitle = Interview.objects.get(id=schedule.interview_id).title
		participantuseremail = Participant.objects.get(id=schedule.participant_id).useremail
		for object in jsonArr:
			if object['title'] == interviewtitle:
				object['participants'].append(participantuseremail)

	tmp=[]
	for i in jsonArr:
		if i not in tmp:
			tmp.append(i)
	
	jsonArr.clear()
	jsonArr.extend(tmp)
	    
	return jsonArr

def getallinterviewsapi(request):
	
	
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
	date = request.POST['date']
	starttime = request.POST['starttime']
	endtime = request.POST['endtime']
	flag,msg = isValidSchedule(list(participants),date,starttime,endtime)

	if isValidCount(list(participants)) == False:
		data = {
		"errormsg" : "Number of participants are less than 2"
		}
		return render(request,'index.html',context=data)
	
	elif flag == False:
		data = {
		"errormsg" : msg
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
	allinterviews = getallinterviews()
	data = {
		"allinterviews" : allinterviews,
		"successmsg" : successmsg
	}
	return render(request,'index.html',context=data)
	

def isValidSchedule(currentparticipants,currentdate,currentstarttime,currentendtime):
	allinterviews = getallinterviews()

	for interview in allinterviews:
		print(interview['date'],currentdate)
		if interview['date'] == currentdate:
			for currentparticipant in currentparticipants:
				for participant in interview['participants']:
					if currentparticipant == participant:
						print(currentparticipant)
						if abs(currentstarttime-interview['endtime']) <= 1 or abs(currentstarttime-interview['endtime']):
							errormsg = "{} has already an interview scheduled at {} on {}".format(participant,interview['endtime'],interview['date'])
							return (False,errormsg)

	return (True,"")

def isValidCount(participants):
	if len(participants) < 2:
		return False
	else:
		return True

# Create your views here.
