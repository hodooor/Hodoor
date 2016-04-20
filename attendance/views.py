from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from .serializers import SwipeSerializer,UserSerializer,KeySerializer
from .models import Swipe, Key, Session
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

def home_page(request):
	return HttpResponse(
		'<html><head><title>ticker</title></head><body><h1>Swipes</h1></body></html>'
	)

class SwipeViewSet(viewsets.ModelViewSet):
	'''
	API end point for posting swipes
	'''
	queryset = Swipe.objects.all()
	serializer_class = SwipeSerializer
	http_method_names = ['post','get']

class KeyViewSet(viewsets.ModelViewSet):
	queryset = Key.objects.all()
	serializer_class = KeySerializer
	http_method_names = ['get',]

class SessionList(ListView):
	queryset = Session.objects.all()
	context_object_name = 'my_favorite_sessions'
	# def get_context_data(self, **kwargs):
	# #     # Call the base implementation first to get a context
	#      context = super(SessionList, self).get_context_data(**kwargs)
	# #     # Add in the publisher
	#      context['swipe'] = self..swipe_set.all()
	#      return context

class SessionDetail(DetailView):
	#model = Session
	queryset = Session.objects.get(id= 73)
	# context_object_name = 'session'
	# def get_context_data(self, **kwargs):
 # 		context = super(PublisherDetail, self).get_context_data(**kwargs)
 # 		context['swipe_list'] = Swipe.objects.all()
 # 		return context