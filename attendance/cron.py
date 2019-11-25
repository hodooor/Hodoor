from django.contrib.auth.models import User
from .models import Session
from django.core.mail import send_mass_mail
from attendance.utils import get_quota_work_hours, get_num_of_elapsed_workdays_in_month, get_number_of_work_days, last_month
from datetime import datetime, date
from django.template.loader import get_template


def send_notifications():
    messages = ()
    text_last_month = get_template('notifications/last_month_notification_email.txt')
    text_end_of_month = get_template('notifications/end_of_month_notification_email.txt')
 
    last_month_ = last_month()
    today = date.today()
    if last_month == 12:
        last_month_year = today.year - 1
    else:
        last_month_year = today.year
        
    for u in User.objects.all():
        hours_unassigned_last_month = Session.objects.get_unassigned_hours_month(u.id, last_month_, last_month_year)

        if hours_unassigned_last_month > 0:
            content = text_last_month.render({
                    'user': u,
                    'hours': hours_unassigned_last_month,
                    'date': today,
                })
            messages += (("Unassigned hours",
                          content,
                          "ho.door@eledus.cz",
                          [u.email]
                          ),)

    num_of_elapsed_workdays = get_num_of_elapsed_workdays_in_month(today)
    num_of_workdays = get_number_of_work_days(today.year, today.month)

    if num_of_workdays - num_of_elapsed_workdays <= 20:
        for u in User.objects.all():
            hours_unassigned_this_month = Session.objects.get_unassigned_hours_month(u.id, today.month, today.year)

            if hours_unassigned_this_month > 0:
                content = text_end_of_month.render({
                        'user': u,
                        'hours': hours_unassigned_this_month,
                        'date': today,
                    })
                messages += (("Assign hours",
                              content,
                              "ho.door@eledus.cz",
                              [u.email]
                              ),)

    send_mass_mail(messages, fail_silently=False)


    
