from factory import DjangoModelFactory, Sequence, PostGenerationMethodCall
from factory import  LazyFunction, LazyAttribute, SubFactory, fuzzy
from factory.django import mute_signals
from django.contrib.auth.hashers import make_password
from attendance.models import Swipe
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime
from faker import Factory
from django.utils import timezone
from django.db.models.signals import post_save

faker = Factory.create()
swipe_types = [short_type[0] for short_type in Swipe.SWIPE_TYPES]


class UserFactory(DjangoModelFactory):

	class Meta:
		model = User

	first_name = LazyFunction(faker.first_name)
	last_name = LazyFunction(faker.last_name)
	username = LazyAttribute(lambda o: slugify(o.first_name) + "." + slugify(o.last_name))
	email = LazyAttribute(lambda o: o.username + "@eledus.cz")
	password = PostGenerationMethodCall('set_password', 'password')
	is_staff = False
	is_superuser = False

#@mute_signals(post_save)
class SwipeFactory(DjangoModelFactory):
	class Meta:
		model = Swipe
	
	user = SubFactory(UserFactory)	
	datetime = LazyFunction(timezone.now)
	swipe_type = fuzzy.FuzzyChoice(swipe_types)
	correction_of_swipe = None

