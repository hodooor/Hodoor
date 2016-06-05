"""
This file is meant for quick "shell-like" testing during functions
building
"""

from django.conf import settings

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticker.settings")
django.setup()

from attendance.models import Swipe,Session
from django.contrib.auth.models import User



def print_doc_str_and_return_value(functions_iterable):
	'''
	Takes list of functions and prints thier docstring with retun values
	'''
	for function in functions_iterable:
		print(function.__doc__.strip(), str(function()))

from attendance.factories import UserFactory

user = UserFactory(first_name = "Ondřej", last_name = "Vičar")
print(user.id, user.username, user.email, user.password)
print (type(user))
user = UserFactory(first_name = "Tomáš", last_name = "Matějka")
print(user.id, user.username, user.email, user.password)
