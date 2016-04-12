from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from .serializers import SwipeSerializer
from .models import Swipe

def home_page(request):
	return HttpResponse(
		'<html><head><title>ticker</title></head><body><h1>Swipes</h1></body></html>'
	)

class SwipeViewSet(viewsets.ModelViewSet):
	'''
	API end point for posting users
	'''
	queryset = Swipe.objects.all()
	serializer_class = SwipeSerializer
	#http_method_names = ['get', 'post']
