from factory import DjangoModelFactory, Sequence
from django.contrib.auth.hashers import make_password
from attendance.models import User
from django.template.defaultfilters import slugify
from factory import DjangoModelFactory, lazy_attribute
import faker

faker = faker.Factory.create()

class UserFactory(DjangoModelFactory):

	class Meta:
		model = User
		django_get_or_create = ("username",)


	first_name = lazy_attribute(lambda o: faker.first_name())
	last_name = lazy_attribute(lambda o: faker.last_name())
	username = lazy_attribute(lambda o: slugify(o.first_name) + "." + slugify(o.last_name))
	email = lazy_attribute(lambda o: o.username + "@eledus.cz")
	password = make_password("password")#make_password ("password")
	# @lazy_attribute
	# def date_joined(self):
	# 	return dt.datetime.now() - dt.timedelta(days=randint(5, 50)
	
	# last_login = lazy_attribute(lambda o: o.date_joined + dt.timedelta(days=4))