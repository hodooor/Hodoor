from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
	return HttpResponse(
		'<html><head><title>ticker</title></head><body><h1>Swipes</h1></body></html>'
	)
