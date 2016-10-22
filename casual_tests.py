"""
This file is meant for quick "shell-like" testing during functions
building
"""

from django.conf import settings
import time
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticker.settings")
django.setup()

from attendance.models import Swipe, Session
from django.contrib.auth.models import User
from attendance import factories

from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime
from attendance.managers import SessionManager

def print_doc_str_and_return_value(functions_iterable):
    '''
    Takes list of functions and prints thier docstring with retun values
    '''
    for function in functions_iterable:
        print(function.__doc__.strip(), str(function()))
now = time.time()

user = User.objects.get(username="ondrej.vicar")
month = datetime.now().month-1

Session.objects.get_sessions_month(user, month)