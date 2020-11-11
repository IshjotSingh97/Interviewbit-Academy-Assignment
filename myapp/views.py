from django.shortcuts import render
from django.http import JsonResponse,HttpResponse


def testserver(request):
	return HttpResponse("Sever has started successfully")

def index(request):
	return render(request,'index.html')

def onsubmit(request):
	return JsonResponse(request.POST)

def isValidCount(participants):
	participants = participants.split(',')
	if len(participants) < 2:
		errormsg = "Number of participants are less than 2"
		return (False,errormsg)
	else:
		validmsg = "This schedule is valid"
		return (True,validmsg)

# Create your views here.
