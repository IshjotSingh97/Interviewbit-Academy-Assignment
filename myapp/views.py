from django.shortcuts import render
from django.http import JsonResponse,HttpResponse


def testServer(request):
	return HttpResponse("Sever has started")

def index(request):
	return render(request,'index.html')

def onSubmit(request):
	data = {
	"title" : request.POST["title"],
	"useremail":request.POST['useremail']
	}
	return JsonResponse(data)

# Create your views here.
