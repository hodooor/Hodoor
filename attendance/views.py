from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from rest_framework import viewsets
from .serializers import SwipeSerializer,UserSerializer,KeySerializer
from .models import Swipe, Key, Session
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from rest_framework import permissions

@login_required(login_url='/login/')
def home_page(request):
	return HttpResponseRedirect(
		reverse(user, args=[request.user.username]))

class SwipeViewSet(viewsets.ModelViewSet):
	'''
	API end point for posting swipes
	'''
	queryset = Swipe.objects.all().order_by("-datetime")[:20]
	serializer_class = SwipeSerializer
	http_method_names = ['post','get']
	permission_classes = (permissions.IsAuthenticated,)

class KeyViewSet(viewsets.ModelViewSet):
	queryset = Key.objects.all()
	serializer_class = KeySerializer
	http_method_names = ['get',]
	permission_classes = (permissions.IsAuthenticated,)

# def sessions(request):
# 	sessions_with_swipes  = list()
# 	sessions = Session.objects.all()
	
# 	for session in sessions:
# 		sessions_with_swipes.append([session, session.swipe_set.all()])

# 	print(sessions_with_swipes)

# 	session_list = Session.objects.all()
# 	context = {
# 				"session_list": session_list,
# 				"session_with_swipes": sessions_with_swipes,}
# 	return render(request, "attendance/session_list.html", context)

def user_check(request, username):
	#superuser should be able to see all profiles
	if request.user.get_username() == username or request.user.is_superuser or request.user.is_staff:
		return True
	else:
		return False

@login_required(login_url='/login/')
def user(request, username):
	if not user_check(request, username): 
		return HttpResponse("Restricted to " + username)
	u = User.objects.get(username = username)
	s = Session.objects.filter(user__id = u.id)
	context = {	"user" : u, 
				"session_list":s,
				"hours_this_month": Session.objects.get_hours_this_month(u.id),}
	return render(request, "attendance/user_page.html", context)

@login_required(login_url='/login/')
def sessions(request, username):
	if not user_check(request, username): 
		return HttpResponse("Restricted to " + username)
	sessions = Session.objects.filter(user__username = username)
	context = {
		"sessions":sessions,
		
	}
	return render(request, "attendance/sessions.html", context)

def swipes(request, username):
	if not user_check(request, username): 
		return HttpResponse("Restricted to " + username)
	context = {}
	return render(request, "attendance/swipes.html", context)