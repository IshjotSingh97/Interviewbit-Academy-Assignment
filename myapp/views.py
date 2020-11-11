from django.shortcuts import render
from django.http import JsonResponse,HttpResponse


def testserver(request):
	return HttpResponse("Sever has started")

def index(request):
	return render(request,'index.html')

def onsubmit(request):
	return JsonResponse(request.POST)

# Create your views here.
