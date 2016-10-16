from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand
from attendance.factories import UserFactory
from django.test import Client

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username')
        #parser.add_argument('password')

    def handle(self, *args, **options):
        session_key = create_pre_authenticated_session(options['username'])
        self.stdout.write(session_key)

def create_pre_authenticated_session(username):
    client = Client()

    user = UserFactory(username=username, password="password")


    client.login(username = user.username, password="password")

    return client.session.session_key
