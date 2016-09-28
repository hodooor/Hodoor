from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from rest_framework import viewsets
from .serializers import SwipeSerializer,UserSerializer,KeySerializer
from .models import Swipe, Key, Session,ProjectSeparation, Project
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from rest_framework import permissions
from datetime import datetime
from .forms import ProjectSeparationForm, SwipeEditForm
from django.utils import timezone
from django.db.models import Q

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
	if request.method == "POST":
		if request.POST.get("IN"):
			Swipe.objects.create(
				swipe_type = "IN",
				user = request.user,
				datetime = timezone.now(),
			)
		if request.POST.get("OUT"):
			Swipe.objects.create(
				swipe_type = "OUT",
				user = request.user,
				datetime = timezone.now(),
			)
		if request.POST.get("OBR"):
			Swipe.objects.create(
				swipe_type = "OBR",
				user = request.user,
				datetime = timezone.now(),
			)
		if request.POST.get("FBR"):
			Swipe.objects.create(
				swipe_type = "FBR",
				user = request.user,
				datetime = timezone.now(),
			)
		if request.POST.get("OTR"):
			Swipe.objects.create(
				swipe_type = "OTR",
				user = request.user,
				datetime = timezone.now(),
			)
		if request.POST.get("FTR"):
			Swipe.objects.create(
				swipe_type = "FTR",
				user = request.user,
				datetime = timezone.now(),
			)
	u = User.objects.get(username = username)
	s = Session.objects.get_sessions_this_month(user = u)


	open_sessions = Session.objects.get_open_sessions()

	latest_swipes = []

	for session in open_sessions:
		latest_swipes.append(
			Swipe.objects.filter(session = session).order_by("-datetime")[0]
		)

	at_work_users, on_break_users, on_trip_users = [],[],[]

	for swipe in latest_swipes:
		if swipe.swipe_type == "IN" or swipe.swipe_type == "FBR" or swipe.swipe_type == "FTR":
			at_work_users.append(swipe.user)
		elif swipe.swipe_type == "OBR":
			on_break_users.append(swipe.user)
		elif swipe.swipe_type == "OTR":
			on_trip_users.append(swipe.user)

	try:
		last_swipe = Swipe.objects.filter(user = u).order_by("-datetime")[0]
		next_swipes = last_swipe.get_next_allowed_types()
	except IndexError:
		last_swipe = None
		next_swipes = None

	context = {	"user" : u,
				"session_list":s,
				"hours_this_month": Session.objects.get_hours_this_month(u.id),
				"last_swipe": last_swipe,
				"next_swipes": next_swipes,
				"at_work_users": at_work_users,
				"on_break_users": on_break_users,
				"on_trip_users": on_trip_users
	}
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
	swipes = Swipe.objects.filter(
		user__username = username,
		session__isnull = False,
	)

	context = {"swipes":swipes}
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
	u = User.objects.get(username = username)


	separations = ProjectSeparation.objects.filter(session__in = sessions)

	projects = dict()

	for separation in separations:
		if separation.project.name in projects.keys():
			projects[separation.project.name] += separation.time_spend.seconds/3600
		else:
			projects[separation.project.name] = separation.time_spend.seconds/3600

	context = {
		"sessions":sessions,
		"year":year,
		"month":month,
		"hours_selected_month": Session.objects.get_hours_month(u.id, month),
		"unassigned_hours": Session.objects.get_unassigned_hours_month(u.id, month),
		"list_of_projects": projects,
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

		return_url = reverse("sessions_month", kwargs={
			'username': username,
			'year': str(session.get_date().year),
			'month': "{0:02d}".format(session.get_date().month, '02d'),
		})

		context = {
			"session":session,
			"id":id,
			"project_separation_form": form,
			"separations":separations,
			"swipes":swipes,
			"return_url": return_url,
		}
		return render(request, "attendance/session_detail.html", context)
	else:
		return HttpResponse("Restricted to " + session.user.username)

@login_required(login_url='/login/')
def swipe_detail(request, username, id):
	if not user_check(request, username):
		return HttpResponse("Restricted to " + username)
	swipe = get_object_or_404(Swipe, pk = int(id))

	if swipe.user.username == username: #write test for this!!

		if request.method == "POST":
			form = SwipeEditForm(request.POST, instance = swipe)

			if form.is_valid():
				cleaned_data = form.cleaned_data
				swipe.datetime = cleaned_data["datetime"]
				Swipe.objects.create(
					user = swipe.user,
					datetime = cleaned_data["datetime"],
					swipe_type = swipe.swipe_type,
					source = "Correction",
					correction_of_swipe = swipe,
				)
		else:
			form = SwipeEditForm(
				initial = {
					"datetime":swipe.datetime,
				}
			)
		if (swipe.swipe_set.all()):
			corrected_by = swipe.swipe_set.all()[0]
		else:
			corrected_by = None
		context={
			"swipe":swipe,
			"id": id,
			"form": form,
			"corrected_by": corrected_by
		}
		return render(request, "attendance/swipe_detail.html", context)
	else:
		return HttpResponse("Restricted to " + session.user.username)

@login_required(login_url='/login/')
def administrator(request, year=str(datetime.now().year), month="{0:02d}".format(datetime.now().month, '02d')):

	user_data = []
	for user in User.objects.all():
		user_data.append({
			"user": user,
			"hours_total": Session.objects.get_hours_month(user.id, month),
			"hours_unassigned": Session.objects.get_unassigned_hours_month(user.id, month),
			"looks_ok": False,
			"hours_assigned": 0
		})
	for user in user_data:
		user["hours_assigned"] = user["hours_total"] - user["hours_unassigned"]
		if user['hours_unassigned'] == 0 and user['hours_total'] > 0:
			user["looks_ok"] = True
		else:
			user["looks_ok"] = False

	context = {
		"month": month,
		"year": year,
		"user_data": sorted(user_data, key=lambda dic: dic["user"].username)
	}
	return render(request, "attendance/administrator.html", context)
