# '''
# For testing posting swipes over REST API
# '''
from django.conf import settings
import requests
import json
import unittest

import time


import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticker.settings")
django.setup()


from attendance.models import Swipe,Session



class ApiPostSwipesTest(unittest.TestCase):


	from datetime import datetime,timedelta

	#generate users
	user = 2 #ondrej.vicar
	
	#generate swipetypes
	#swipe_types = ["IN","OBR","FBR","OUT","IN","OUT","IN","OBR",
	#	"FBR","OBR","FBR","OUT"]
	swipe_types = ["IN","OBR", "FBR","OBR", "FBR","OUT"]
	hours_increment = 4

		#generte datetimes
	datetimes = []
	t = datetime.now()

	for swipe in swipe_types:
		datetimes.append((t + timedelta(hours = hours_increment)).isoformat())
		hours_increment += 4
	
	data = []

	for swipe_type,datetime, in zip(swipe_types,datetimes):
		data.append({"user":user,"swipe_type":swipe_type,"datetime":datetime})	
	
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

		for swipe in self.data:
			r = requests.post(POST_URL, json.dumps(swipe), headers = HEADERS)
			self.assertEqual(r.status_code,201) #CREATED 201
		
		s = Swipe.objects.all()
		
		#self.assertEqual(1,500)
		for swipe,data_constant in zip(s,self.data):
			self.assertEqual(swipe.user.id,data_constant["user"])
			
			self.assertEqual(swipe.swipe_type,data_constant["swipe_type"])
			self.assertEqual(swipe.datetime.isoformat()[:-6],data_constant["datetime"])


if __name__ == '__main__':
	# a = ApiPostSwipesTest()
	# a.post_some_swipes()
	# a.get_posted_data_from_database()
	unittest.main()
	#print(Session.objects.all(),Swipe.objects.all())
