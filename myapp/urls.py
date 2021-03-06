from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
	path('tesservert',views.testserver,name='testserver'),
	path('',views.index,name='index'),
	path('onsubmit',views.onsubmit,name='onsubmit'),
	path('getallinterviewsapi',views.getallinterviewsapi,name='getallinterviewsapi'),
	path('deleteinterview/<str:title>',views.deleteinterview,name='deleteinterview'),
	path('updateinterview/<str:title>',views.updateinterview,name='updateinterview')
]