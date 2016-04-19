# '''
# For testing posting swipes over REST API
# '''
from django.conf import settings
import requests
import json
import unittest
import time
from datetime import timedelta,datetime
from random import randint
from const_data import USERS, SWIPES


import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticker.settings")
django.setup()


from attendance.models import Swipe,Session



class ApiPostSwipesTest(unittest.TestCase):


	from datetime import datetime,timedelta

	def setUp(self):
		Swipe.objects.all().delete()
		print("Swipes deleted from database")
		Session.objects.all().delete()
		print("Sessions deleted from database")
	
	def tearDown(self):
		print("Tore Down!")	
			
	
	def test_post_some_swipes(self):
		"""
		Populates database with some swipes thru REST API
		"""
	
		POST_URL = "http://127.0.0.1:8000/swipes/"
		HEADERS = {'Content-Type': 'application/json'}

		for swipe in SWIPES:
			r = requests.post(POST_URL, json.dumps(swipe), headers = HEADERS)
			self.assertEqual(r.status_code,201) #CREATED 201
		
		s = Swipe.objects.all()
		
		for swipe_database, swipe_const in zip(s,SWIPES):
			self.assertEqual(swipe_database.user.id, int(swipe_const["user"]))		
			self.assertEqual(swipe_database.swipe_type,swipe_const["swipe_type"])
			self.assertEqual(swipe_database.datetime.isoformat()[:-6],swipe_const["datetime"])




if __name__ == '__main__':
	unittest.main()

