from django.shortcuts import render
from django.http import JsonResponse,HttpResponse


def test(request):
	return HttpResponse("Sever started on localhost")

def index(request):
	return render(request,'index.html')

def onSubmit(request):
	data = {
	"title" : request.POST["title"],
	"useremail":request.POST['useremail']
	}
	return JsonResponse(data)

# Create your views here.
