from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timezone, timedelta
from .managers import SessionManager, HolidayManager
from django.core.validators import MinValueValidator, MaxValueValidator
from .utils import is_workday, get_number_of_work_days_in_daterange


class Project(models.Model):
    name = models.CharField(max_length=40)

    # so we can define private projects (hours private this project does not count)
    private = models.BooleanField(default=False)
    description = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    def __str__(self):
        """Just name of project."""
        return self.name
        
        
class Contract(models.Model):
    contract_type = models.CharField(
        max_length=20,
        null=False,
        blank=False
    )
    hours_quota = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(8),
            MinValueValidator(0)
        ]
     )
    
    def __str__(self):
        """Just contract type."""
        return self.contract_type
        
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contracts = models.ManyToManyField(Contract)
    aviable_holidays = models.FloatField("Already aviable holidays in hours", default=0)
    days_of_holidays_per_year = models.IntegerField(default=20)

    def create_profile(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            user_profile = Profile(user=user, aviable_holidays = 0, )
            user_profile.save()
    post_save.connect(create_profile, sender=User)

    def get_hours_quota(self):
        hours = 0
        for contract in self.contracts.all():
            hours += contract.hours_quota
        return hours
        
    def get_hours_of_holidays(self, verified = True, year = None):
        hours = 0
        for holiday in self.holidays.all():
            if (year == None) or (year == holiday.date_since.year):
                if holiday.verified == verified:
                    hours += holiday.hours_spend()
        return hours
        
    def get_aviable_holidays_this_year(self, nonverified = False):
        hours_work_this_year = Session.objects.get_hours_this_year(self.user.id)
        if nonverified:
            hours_work_this_year += self.get_hours_of_holidays(year = datetime.now().year, verified = False)
        hours_work_this_year += self.get_hours_of_holidays(year = datetime.now().year)
        hours = self.count_holidays_from_num_of_hours(hours_work_this_year)
        return hours
    
    def need_for_holiday(self):
        i = 0
        dangerous_date = datetime(year = datetime.now().year, month = 12, day = 31)
        num_of_days = (self.get_hours_of_holidays_aviable_to_take()/self.get_hours_quota())+5
        while (i < num_of_days) or (dangerous_date.weekday() != 0):
            dangerous_date -= timedelta(days = 1)
            if is_workday(dangerous_date):
                i += 1
        if datetime.now() > dangerous_date:
            return True
        return False
    
    def get_hours_of_holidays_aviable_to_take(self):
        hours = self.get_aviable_holidays_this_year(nonverified = True) + self.aviable_holidays
        hours -= self.get_hours_of_holidays(verified = True)
        hours -= self.get_hours_of_holidays(verified = False)
        bonus = self.count_holidays_from_num_of_hours(hours)
        while bonus >= 0.01:
            hours += bonus
            bonus = self.count_holidays_from_num_of_hours(bonus)
        return hours
        
    def count_holidays_from_num_of_hours(self, hours):
        days_in_year = get_number_of_work_days_in_daterange(
                datetime(year = datetime.now().year, month = 1, day=1),
                datetime(year = datetime.now().year, month = 12, day=31)
        )
        return round(hours / 260) * (self.days_of_holidays_per_year)
        
    def __str__(self):
        """Name of owner of profile and his contracts."""
        text = self.user.username + ":"
        for contract in self.contracts.all():
            text += " " + contract.contract_type + ","
        return text[:-1]
    

class Session(models.Model):
    user = models.ForeignKey(User)
    # this is saved field and exists only for finished sessions
    duration = models.DurationField(null=True, blank=True)
    modified = models.BooleanField(default=False)
    project = models.ManyToManyField(Project, through="ProjectSeparation")
    objects = SessionManager()

    def num_of_breaks(self):
        """Return number of completed breaks during session."""
        obr = self.swipe_set.filter(swipe_type="OBR")
        fbr = self.swipe_set.filter(swipe_type="FBR")
        if len(obr) != len(fbr):
            print("Some breaks are not complete")
        return len(fbr)

    def breaks_duration(self):
        """Return timedelta duration of all breaks."""
        obr = self.swipe_set.filter(swipe_type="OBR")
        fbr = self.swipe_set.filter(swipe_type="FBR")
        duration = timedelta(0)

        for obr_object, fbr_object in zip(obr, fbr):
            duration += fbr_object.datetime - obr_object.datetime

        if len(obr) > len(fbr):  # if we are on break
            duration += datetime.now(timezone.utc) - obr.latest("datetime").datetime

        duration = duration - timedelta(microseconds=duration.microseconds)
        return duration

    def session_duration_overall(self):
        """Return time delta duration of session(including breaks)."""
        login_datetime = self.swipe_set.get(swipe_type="IN").datetime

        if self.is_session_complete():
            end_datetime = self.swipe_set.get(swipe_type="OUT").datetime
        else:
            end_datetime = datetime.now(timezone.utc)

        bla = end_datetime - login_datetime
        bla = bla - timedelta(microseconds=bla.microseconds)
        return bla

    def session_duration(self):
        """Return time delta duration of session(excluding breaks)."""
        return self.session_duration_overall() - self.breaks_duration()

    def is_session_complete(self):
        if(self.swipe_set.filter(swipe_type="OUT").exists()):
            return True
        else:
            return False

    def get_date(self):
        in_datetime = self.swipe_set.all()[0].datetime
        return in_datetime

    def get_assigned_duration(self):
        time_spend_sum = timedelta(0)

        for sep in self.projectseparation_set.all():
            try:
                time_spend_sum += sep.time_spend
            except TypeError as err:
                if "unsupported operand type(s) for" not in str(err):
                    raise
        return time_spend_sum

    def get_not_assigned_duration(self):
        if Swipe.correction_of_swipe: # Need to check this first for corrected IN swipe of active session
            return self.session_duration() - self.get_assigned_duration()
        else:
            if self.duration:
                return self.duration - self.get_assigned_duration()
            else:
                return self.session_duration() - self.get_assigned_duration()

    def get_not_work_duration(self):
        time_spend_sum = timedelta(0)
        for sep in (s for s in self.projectseparation_set.all() if s.project.private):
            try:
                time_spend_sum += sep.time_spend
            except TypeError as err:
                if "unsupported operand type(s) for" not in str(err):
                    raise
        return time_spend_sum
    def get_model_name(self):
        model_name = 'Session'
        return model_name
    def __str__(self):
        """Id and User."""
        return str(self.id) + " " + str(self.user)


class ProjectSeparation(models.Model):
    """So we can time divide our session into more projects."""

    session = models.ForeignKey(Session)
    project = models.ForeignKey(Project)
    description = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    time_spend = models.DurationField()

    def __str__(self):
        return "Session: " + str(self.session) + " Project: " + str(self.project)


class Swipe(models.Model):
    '''
    Swipes are individual key scans of each user
    '''

    SWIPE_TYPES = (
        ("IN","Login"),
        ("OUT","Logout"),
        ("OBR","On Break"),
        ("FBR","From Break"),
        ("OTR","On Trip"),
        ("FTR","From Trip")
    )

    user = models.ForeignKey(User)
    datetime = models.DateTimeField("Datetime of swipe")

    swipe_type = models.CharField(max_length=3, choices = SWIPE_TYPES)

    #session should be specified for correcting swipe
    session = models.ForeignKey(Session,
            null = True,
            blank = True,
            on_delete = models.SET_NULL,
            )
    source = models.CharField(max_length = 5,null = True, blank = True)

    #this points to swipe that is correction of this one
    correction_of_swipe = models.ForeignKey(
            "self",
            on_delete=models.CASCADE,
            blank = True,
            null = True, #if blank, this swipe is the right one
            )


    def get_next_allowed_types(self):
        """
        Returns tupple of types that can be used in next swipe
        """
        if self.swipe_type == "IN":
            return "OBR", "OTR","OUT",
        elif self.swipe_type == "OUT":
            return "IN",
        elif self.swipe_type == "OBR":
            return "FBR",
        elif self.swipe_type == "FBR":
            return "OBR", "OTR","OUT",
        elif self.swipe_type == "OTR":
            return "FTR",
        elif self.swipe_type == "FTR":
            return "OBR", "OTR","OUT",
        else:
            return "0"

    def __str__(self):
        return str(self.id) + " " + self.user.username + " " + self.swipe_type

    def save(self, *args, **kwargs):
        if(self._state.adding and not self.correction_of_swipe):
            try:
                latest_swipe = Swipe.objects.filter(user = self.user).order_by("-datetime")[0]


                if self.swipe_type not in latest_swipe.get_next_allowed_types():
                    raise ValueError("Wrong swipe_type field")
                    return

                if self.datetime < latest_swipe.datetime:
                    raise ValueError("Wrong datetime field")
                    return

            except IndexError:
                #we have no records for given user, this is probably faster than "if"
                pass

        super(Swipe, self).save(*args, **kwargs)

    def get_last_swipe_same_user(self):
        """
        Returns last swipe of same user
        """
        swipes_before = Swipe.objects.filter(
                user = self.user,
                datetime__lt = self.datetime,
                session__isnull = False, #filter out corrected swipes
        )
        if swipes_before:
            return swipes_before.order_by("-datetime")[0]
        else:
            return None

    def get_next_swipe_same_user(self):
        """
        Returns next swipe of same user
        """
        swipes_after = Swipe.objects.filter(
                user = self.user,
                datetime__gt = self.datetime,
                session__isnull = False, #filter out corrected swipes
        )
        if swipes_after:
            return swipes_after.order_by("datetime")[0]
        else:
            return None

    def swipe_types_verbose(self):
        return dict(Swipe.SWIPE_TYPES)[self.swipe_type]

class Key(models.Model):
    '''
    Saves information data about keys.
    '''
    id = models.CharField(max_length = 10, primary_key = True)
    key_type = models.CharField(max_length = 4, null = True, blank = True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.id + " " + self.user.username + " " + self.key_type
        
class Holiday(models.Model):
    '''
    Saves information data about time spended on holidays
    ''' 
    profile = models.ForeignKey(Profile, related_name="holidays")
    date_since = models.DateField(default = None)
    date_to = models.DateField(default = None)
    work_hours = models.FloatField(default = 0)
    verified = models.BooleanField(default = False)
    reason = models.CharField(max_length = 50, null = True, blank = True)
    objects = HolidayManager()
    
    def hours_spend(self):
        hours = 0
        i = 0
        date = self.date_since
        while date <= self.date_to:
            if is_workday(date):
                hours += self.profile.get_hours_quota()
            date += timedelta(days = 1)
        return hours - self.work_hours
        
    def get_date(self):
        return datetime(year = self.date_since.year, month = self.date_since.month, day = self.date_since.day)
    
    def is_in_month(self, month, year):
        if (self.date_to.month >= month and self.date_to.year >= year):
                if (self.date_since.month <= month and self.date_since.year <= year):
                    return True
        return False
        
    def get_model_name(self):
        model_name = 'Holiday'
        return model_name
        
    def get_hours_month(self, month, year):
        i = 0
        date = self.date_since
        hours = 0
        while date <= self.date_to:
            if (int(date.month)== int(month) and int(date.year)==int(year)):
                if is_workday(date):
                    hours += self.profile.get_hours_quota()
            date += timedelta(days = 1)
        if self.date_to + timedelta(days = 1) == date:
            hours -= self.work_hours
        return hours

    def __str__(self):
        return self.profile.user.username + " " + str(self.date_since) + " to " + str(self.date_to) + ": " + str(int(self.hours_spend())) + " hours"



@receiver(post_save, sender = Swipe)
def post_process_swipes(sender=Swipe, **kwargs):
    if kwargs['created']: # trigering only when swipe was created

        #swipe object that was just created
        created_swipe = kwargs["instance"]

        if created_swipe.correction_of_swipe:

            orig_swipe = Swipe.objects.get(id = created_swipe.correction_of_swipe.id)
            orig_swipe.session = None;
            orig_swipe.save()

            created_swipe.session = created_swipe.correction_of_swipe.session
            created_swipe.save()

            created_swipe.session.duration = created_swipe.session.session_duration()
            created_swipe.session.modified = True
            created_swipe.session.save()


        #open new session if created swipe is not correction of old one
        else:
            if created_swipe.swipe_type == "IN":
                sess = Session(user = created_swipe.user)
                sess.save()

                #swipe is related to session
                created_swipe.session = sess
                created_swipe.save()

            #updated oppened session
            else:

                sess = Session.objects.filter(user = created_swipe.user)

                #session without OUT swipe (open session)
                sess = sess.exclude(swipe__swipe_type = "OUT")
                if len(sess) == 1:
                    sess = sess[0]
                else:
                    raise ValueError('More Opened Sessions')

                created_swipe.session = sess
                created_swipe.save()
                if created_swipe.swipe_type == "OUT":
                    sess.duration = sess.session_duration()
                    sess.save()
