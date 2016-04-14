'''
For testing posting swipes over REST API
'''
from django.conf import settings
import requests
import json
import unittest

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticker.settings")
django.setup()


from attendance.models import Swipe



class ApiPostSwipesTest(unittest.TestCase):


	from datetime import datetime,timedelta

	#generate users
	user = 1 #ondrej.vicar
	
	#generate swipetypes
	swipe_types = ["IN","OBR","FBR","OUT","IN","OUT","IN","OBR",
		"FBR","OBR","FBR","OUT"]
	hours_increment = 1

		#generte datetimes
	datetimes = []
	t = datetime.now()

	for swipe in swipe_types:
		datetimes.append((t + timedelta(hours = hours_increment)).isoformat())
		hours_increment += 1 
	
	data = []

	for swipe_type,datetime, in zip(swipe_types,datetimes):
		data.append({"user":user,"swipe_type":swipe_type,"datetime":datetime})	

	
	def test_post_some_swipes(self):
		"""
		Populates database with some swipes thru REST API
		"""
	
		POST_URL = "http://127.0.0.1:8000/swipes/"
		HEADERS = {'Content-Type': 'application/json'}

		#need to crete list of dictionaries:
		

		for swipe in self.data:
			r = requests.post(POST_URL, json.dumps(swipe), headers = HEADERS)
			self.assertEqual(r.status_code,201) #CREATED 201
				#print("POSTED:	" + str(swipe))

	def test_get_posted_data_from_database(self):
		s = Swipe.objects.all()

		for swipe,data_constant in zip(s,self.data):
			self.assertEqual(swipe.user.id,data_constant["user"])
			self.assertEqual(swipe.swipe_type,data_constant["swipe_type"])
			#self.assertEqual(swipe.datetime.isoformat()[:-6],data_constant["datetime"])
		
		Swipe.objects.all().delete() #deletes swipes fomrom database
		self.assertFalse(Swipe.objects.all())
		

	#def tearDown(self):
		#Swipe.objects.all().delete()
#now we want to read if they are in database


if __name__ == '__main__':
	# a = ApiPostSwipesTest()
	# a.post_some_swipes()
	# a.get_posted_data_from_database()
	unittest.main()