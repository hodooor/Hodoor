from django.db.models import Q
from django.db import models
from datetime import datetime, timedelta


class SessionManager(models.Manager):
    def get_sessions_month(self, user, month):
        from .models import Swipe
        """Return List of sessions made inserted month."""
        swipes_month = Swipe.objects.filter(
            swipe_type="IN",
            datetime__month=month,
            user=user
        )

        if swipes_month:
            swipes_list = swipes_month.values_list('id', flat=True)
            sessions = self.model.objects.filter(swipe__in=swipes_list)
            return sessions
        else:
            return 0

    def get_sessions_this_month(self, user):
        """Return List of sessions made this month."""
        return self.get_sessions_month(user, datetime.now().month)

    def get_hours_month(self, user, month):
        """Return number of hours in selected month (already finished sessions)."""
        sessions_month = self.get_sessions_month(user, month)
        if(sessions_month):
            new_dur = timedelta(0)
            for session in sessions_month:
                if(session.duration):
                    new_dur += session.duration
            return new_dur.total_seconds()/3600
        else:
            return 0

    def get_hours_this_month(self, user):
        """Return number of hours this month (already finished sessions)."""
        return self.get_hours_month(user, datetime.now().month)

    def get_unassigned_hours_month(self, user, month):
        sessions_month = self.get_sessions_month(user, month)
        if(sessions_month):
            new_dur = timedelta(0)
            for session in sessions_month:
                new_dur += session.get_not_assigned_duration()
            return new_dur.total_seconds()/3600
        else:
            return 0

    def get_not_work_hours_month(self, user, month):
        sessions_month = self.get_sessions_month(user, month)
        if(sessions_month):
            new_dur = timedelta(0)
            for session in sessions_month:
                new_dur += session.get_not_work_duration()
            return new_dur.total_seconds()/3600
        else:
            return 0

    def get_open_sessions(self):
        return self.model.objects.filter(~Q(swipe__swipe_type='OUT'))
