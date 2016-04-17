from django.conf import settings

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticker.settings")
django.setup()

from attendance.models import Swipe,Session

s = Session.objects.all()[0]

dur = s.session_duration
over = s.session_duration_overall
num = s.num_of_breaks
bdur = s.breaks_duration

def print_doc_str_and_return_value(functions_iterable):
	'''
	Takes list of functions and prints thier docstring with retun values
	'''
	for function in functions_iterable:
		print(function.__doc__.strip(), str(function()))

print_doc_str_and_return_value([dur,over,num,bdur])


