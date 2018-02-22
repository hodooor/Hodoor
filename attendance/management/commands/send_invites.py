from django.core.management.base import BaseCommand
from attendance.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

class Command(BaseCommand):
    msg_plain = render_to_string('registration/invitation_email.txt', {'site_name': "hodoor.eledus.cz"})
    msg_html = render_to_string('registration/invitation_email.html', {'site_name': "hodoor.eledus.cz"})

    users = User.objects.all()
    for user in users:
        if not user.last_login: # was never loged in
            print("Sending invite email to " + user.email)
            send_mail(
                    subject = "Welcome to Hodoor",
                    message = msg_plain,
                    from_email = "ho.door@eledus.cz",
                    recipient_list = [user.email],
                    auth_user = "ho.door@eledus.cz",
                    fail_silently = False,
                    html_message = msg_html,
            )

    def handle(self, *args, **options):
        pass
