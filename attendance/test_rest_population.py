'''
For testing posting swipes over REST API
'''

import requests
import json
import unittest


def post_some_swipes():
	"""
	Populates database with some swipes thru REST API
	"""
	from datetime import datetime,timedelta

	POST_URL = "http://127.0.0.1:8000/swipes/"
	HEADERS = {'Content-Type': 'application/json'}


	#generate users
	user = 1 #ondrej.vicar

	#generte datetimes
	datetimes = []
	t = datetime.now()
	#generate swipetypes
	swipe_types = ["IN","OBR","FBR","OUT","IN","OUT","IN","OBR","FBR","OBR","FBR","OUT"]
	hours_increment = 1

	for swipe in swipe_types:
		datetimes.append((t + timedelta(hours = hours_increment)).isoformat())
		hours_increment += 1 



	#need to crete list of dictionaries:
	data = []

	for swipe_type,datetime, in zip(swipe_types,datetimes):
		data.append({"user":user,"swipe_type":swipe_type,"datetime":datetime})

	for swipe in data:
		r = requests.post(POST_URL, json.dumps(swipe), headers = HEADERS)
		if(r.status_code == 201): #CREATED 201
			print("POSTED:	" + str(swipe))

#now we want to read if they are in database
if __name__ == '__main__':
	post_some_swipes()
