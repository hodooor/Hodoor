from django.core.management.base import BaseCommand
from attendance.models import User

EMAIL_DOMAIN = "eledus.cz"

class Command(BaseCommand):
	users = User.objects.all()
	for user in users:
		if not user.email:
			print("User " + user.username + " has no email. Creating one...")
			user.email = user.username + "@" + EMAIL_DOMAIN
			user.save()
			print("Email " + user.email + " created.")
		else:
			print("User " + user.username + " already has email.")

	def handle(self, *args, **options):
		pass