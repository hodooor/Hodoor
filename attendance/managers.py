from django.db.models import Q
from django.db import models
from datetime import datetime, timedelta


class SessionManager(models.Manager):
    def get_sessions_month(self, user, month):
        sessions = self.model.objects.filter(
            user=user,
            swipe__datetime__month=month,
            swipe__swipe_type="IN"
        ).prefetch_related("swipe_set").prefetch_related("projectseparation_set")
        return sessions

    def get_sessions_this_month(self, user):
        return self.get_sessions_month(user, datetime.now().month)

    def get_hours_month(self, user, month, sessions_month=None):
        if not sessions_month:
            sessions_month = self.get_sessions_month(user, month)
        if sessions_month:
            new_dur = timedelta(0)
            for session in sessions_month:
                if session.duration:
                    new_dur += session.duration
                else:
                    new_dur += session.session_duration()
            return new_dur.total_seconds()/3600
        else:
            return 0

    def get_hours_this_month(self, user):
        """Return number of hours this month (already finished sessions)."""
        return self.get_hours_month(user, datetime.now().month)

    def get_unassigned_hours_month(self, user, month, sessions_month=None):
        if not sessions_month:
            sessions_month = self.get_sessions_month(user, month)
        if(sessions_month):
            new_dur = timedelta(0)
            for session in sessions_month:
                new_dur += session.get_not_assigned_duration()
            return new_dur.total_seconds()/3600
        else:
            return 0

    def get_not_work_hours_month(self, user, month, sessions_month=None):
        if not sessions_month:
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
