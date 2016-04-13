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
	
	#generte datetimes
	datetimes = []
	t = datetime.now()
	
	#generate swipetypes
	swipe_types = ["IN","OBR","FBR","OUT","IN","OUT","IN","OBR",
		"FBR","OBR","FBR","OUT"]
	hours_increment = 1

	for swipe in swipe_types:
		datetimes.append((t + timedelta(hours = hours_increment)).isoformat())
		hours_increment += 1 
	
	def post_some_swipes(self):
		"""
		Populates database with some swipes thru REST API
		"""
		

		POST_URL = "http://127.0.0.1:8000/swipes/"
		HEADERS = {'Content-Type': 'application/json'}

		#need to crete list of dictionaries:
		data = []

		for swipe_type,datetime, in zip(self.swipe_types,self.datetimes):
			data.append({"user":self.user,"swipe_type":swipe_type,"datetime":datetime})

		for swipe in data:
			r = requests.post(POST_URL, json.dumps(swipe), headers = HEADERS)
			if(r.status_code == 201): #CREATED 201
				print("POSTED:	" + str(swipe))

	def get_posted_data_from_database(self):
		s = Swipe.objects.all()

		for swipe in s:
			print(swipe)
		s.delete()


#now we want to read if they are in database


if __name__ == '__main__':
	a = ApiPostSwipesTest()
	a.post_some_swipes()
	a.get_posted_data_from_database()
