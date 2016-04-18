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

def generate_random_datetimes_for_swipes(swipes):
	'''
	Generates pseudorandom list of datetimes in chronological order for testing 
	purposes in string isoformat.
	'''
	from datetime import timedelta,datetime
	datetimes = []
	t = datetime.now()

	for swipe in swipes:
		timd = timedelta(
			hours = randint(0,4),
			minutes = randint(0,59),
			seconds = randint(0,59),
		)

		t += timd
		
		datetimes.append(t.isoformat())

	return datetimes

class ApiPostSwipesTest(unittest.TestCase):


	from datetime import datetime,timedelta

	#generate users
	user = 2 #ondrej.vicar
	
	#generate swipetypes
	#swipe_types = ["IN","OBR","FBR","OUT","IN","OUT","IN","OBR",
	#	"FBR","OBR","FBR","OUT"]
	swipe_types = ["IN","OBR", "FBR","OBR", "FBR","OUT"]

	datetimes = generate_random_datetimes_for_swipes(swipe_types) 
	
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

		for swipe in SWIPES:
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
	print(USERS)
	print(SWIPES)
	unittest.main()
	#print(Session.objects.all(),Swipe.objects.all())
