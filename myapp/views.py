from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from datetime import *
from .models import *
import collections
import re

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

	if isValidEmail(participants):
		pass
	else:
		data = {
		"errormsg" : "Only emails allowed"
		}
		return render(request,'index.html',context=data)

	date = request.POST['date']
	starttime = request.POST['starttime']
	endtime = request.POST['endtime']

	if starttime > endtime:
		data = {
		"errormsg" : "Startime {} is greater than Endtime {}".format(starttime,endtime)
		}
		return render(request,'index.html',context=data)

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
		interview['date'] = interview['date'].strftime('%Y-%m-%d')
		d1 = interview['date']
		d2 = currentdate
		if d1 == d2:
			for currentparticipant in currentparticipants:
				for participant in interview['participants']:
					if currentparticipant == participant:
						t1 = interview['starttime']
						t2 = interview['endtime']
						t3 = datetime.strptime(currentstarttime, '%H:%M').time()
						t4 = datetime.strptime(currentendtime, '%H:%M').time()
						# Create datetime objects for each time (a and b)
						dateTimeA = datetime.combine(date.today(), t1)
						dateTimeB = datetime.combine(date.today(), t4)
						# Get the difference between datetimes (as timedelta)
						dateTimeDifference = abs(dateTimeA - dateTimeB)
						# Divide difference in seconds by number of seconds in hour (3600)  
						dateTimeDifferenceInHours1 = dateTimeDifference.total_seconds() / 3600
						
						dateTimeA = datetime.combine(date.today(), t3)
						dateTimeB = datetime.combine(date.today(), t4)
						# Get the difference between datetimes (as timedelta)
						dateTimeDifference = abs(dateTimeA - dateTimeB)
						# Divide difference in seconds by number of seconds in hour (3600)  
						dateTimeDifferenceInHours2 = dateTimeDifference.total_seconds() / 3600
				
						if dateTimeDifferenceInHours1 <= 1 or dateTimeDifferenceInHours2 <= 2:
							errormsg = "{} has already an interview scheduled on {} between {} and {}".format(participant,d1,t1,t2)
							return (False,errormsg)

	return (True,"")

def isValidCount(participants):
	if len(participants) < 2:
		return False
	else:
		return True


def isValidEmail(participants):
	regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
	for email in participants:
		if not re.search(regex,email):
			return False
	return True

def deleteinterview(request,title):
	interview = Interview.objects.get(title=title)
	schedule = Schedule.objects.filter(interview_id=interview.id)
	print(interview,schedule)
	interview.delete()
	schedule.delete()
	data = {
	"successmsg" : "Interview schedule deleted successfully" 
	}
	return render('index.html',context=data)
