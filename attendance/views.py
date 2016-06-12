from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from rest_framework import viewsets
from .serializers import SwipeSerializer,UserSerializer,KeySerializer
from .models import Swipe, Key, Session,ProjectSeparation
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from rest_framework import permissions
from datetime import datetime
from .forms import ProjectSeparationForm

@login_required(login_url='/login/')
def home_page(request):
	return HttpResponseRedirect(reverse(user, args=[request.user.username]))
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
	now =datetime.now()
	year_str = str(now.year)
	month_str = "{:02}".format(now.month)
	return HttpResponseRedirect(
		reverse(sessions_month, args=[request.user.username, year_str, month_str]))


@login_required(login_url='/login/')
def swipes(request, username):
	if not user_check(request, username): 
		return HttpResponse("Restricted to " + username)
	context = {}
	return render(request, "attendance/swipes.html", context)

@login_required(login_url='/login/')
def sessions_month(request, username, year=datetime.now().year, month = datetime.now().month):
	if not user_check(request, username): 
		return HttpResponse("Restricted to " + username)
	#swipes_this_month = Swipe.objects.filter(swipe_type="IN", datetime__month=datetime.now().month)
	in_swipes_ids = Swipe.objects.filter(
		swipe_type = "IN", 
		user__username = username,
		datetime__month = int(month),
		datetime__year = int(year), 
	).values_list('session', flat=True)
	sessions = Session.objects.filter(pk__in = in_swipes_ids)

	context = {
		"sessions":sessions,
		"year":year,
		"month":month
	}
	return render(request, "attendance/sessions.html", context)

@login_required(login_url='/login/')
def session_detail(request, username, id):
	if not user_check(request, username): 
		return HttpResponse("Restricted to " + username)
	session = get_object_or_404(Session, pk = int(id))
	
	if session.user.username == username: #write test for this!!

		separations =  ProjectSeparation.objects.filter(session = session)
		swipes = Swipe.objects.filter(session = session)
		if request.method == "POST":
			form = ProjectSeparationForm(request.POST)			
			if form.is_valid():
				form.save()
			
		form = ProjectSeparationForm(
			initial={
				"time_spend":session.get_not_assigned_duration(),
				"session": session.id #hidden form 
			},
		)
		context = {
			"session":session,
			"id":id,
			"project_separation_form": form,
			"separations":separations,
			"swipes":swipes
		}
		return render(request, "attendance/session_detail.html", context)
	else:
		return HttpResponse("Restricted to " + session.user.username) 
