from factory import DjangoModelFactory, Sequence, PostGenerationMethodCall, lazy_attribute
from django.contrib.auth.hashers import make_password
from attendance.models import User
from django.template.defaultfilters import slugify
import faker

faker = faker.Factory.create()

class UserFactory(DjangoModelFactory):

	class Meta:
		model = User

	first_name = lazy_attribute(lambda o: faker.first_name())
	last_name = lazy_attribute(lambda o: faker.last_name())
	username = lazy_attribute(lambda o: slugify(o.first_name) + "." + slugify(o.last_name))
	email = lazy_attribute(lambda o: o.username + "@eledus.cz")
	password = PostGenerationMethodCall('set_password', 'password')
	is_staff = lazy_attribute(lambda o: False)
	is_superuser = lazy_attribute(lambda o: False)