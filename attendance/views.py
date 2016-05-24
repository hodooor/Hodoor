from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.core.urlresolvers import reverse
from rest_framework import viewsets
from .serializers import SwipeSerializer,UserSerializer,KeySerializer
from .models import Swipe, Key, Session
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def home_page(request):
	return HttpResponseRedirect(
		reverse(sessions, args=[request.user.username]))

class SwipeViewSet(viewsets.ModelViewSet):
	'''
	API end point for posting swipes
	'''
	queryset = Swipe.objects.all().order_by("-datetime")[:20]
	serializer_class = SwipeSerializer
	http_method_names = ['post','get']

class KeyViewSet(viewsets.ModelViewSet):
	queryset = Key.objects.all()
	serializer_class = KeySerializer
	http_method_names = ['get',]

def sessions(request):
	sessions_with_swipes  = list()
	sessions = Session.objects.all()
	
	for session in sessions:
		sessions_with_swipes.append([session, session.swipe_set.all()])

	print(sessions_with_swipes)

	session_list = Session.objects.all()
	context = {"session_list": session_list, "session_with_swipes": sessions_with_swipes}
	return render(request, "attendance/session_list.html", context)

def user(request, username):
	u = User.objects.get(username = username)
	s = Session.objects.filter(user__id = u.id)
	context = {"user" : u, "session_list":s}
	return render(request, "attendance/user_page.html", context)