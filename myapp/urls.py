from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
	path('test',views.test,name='test'),
	path('',views.index,name='index'),
	path('onsubmit',views.onSubmit,name='onsubmit')
]