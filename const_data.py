from random import randint


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

USERS = [
	{"username":"ondrej.vicar", "id":"1"},
	{"username":"jaroslav.malec", "id":"2"},
	{"username":"lukas.krcma", "id":"3"},
	{"username":"david.binko", "id":"4"},
]
SWIPE_TYPES = ("IN","OBR", "FBR","OBR", "FBR","OUT")
#now generate swipe list of dictionaries
SWIPES = []
for user_id in (d['id'] for d in USERS):
	
	datetime = generate_random_datetimes_for_swipes(SWIPE_TYPES)
	
	for swipe_type,datetime in zip(SWIPE_TYPES,datetime):
		SWIPES.append({
			"user":user_id,
			"swipe_type":swipe_type,
			"datetime":datetime,
		})