from django.core.urlresolvers import resolve
from django.test import TestCase,Client
from attendance.views import home_page
from django.contrib.auth.models import User
from unittest import skip
from django.core.urlresolvers import reverse

from django.http import HttpRequest
from .models import Session, Swipe, Project, ProjectSeparation
from const_data import generate_random_datetimes_for_swipes
from .serializers import SwipeSerializer, UserSerializer
from const_data import USERS, SWIPES, SWIPE_TYPES
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import status
import pytz
from datetime import date
from time import sleep

from attendance.views import sessions_month
from attendance.factories import UserFactory, SwipeFactory, ProjectFactory, ProjectSeparationFactory
from .forms import SwipeEditForm
from .utils import get_num_of_elapsed_workdays_in_month, last_month, daily_hours

def dict_to_database(serializer_class, list_of_dict):
    '''
    Input is serializer class type object and list of dictionaries
    save to database
    '''
    for diction in list_of_dict:
        ser = serializer_class(data = diction)
        ser.is_valid()
        ser.save()

class SessionTestCase(TestCase):
    '''
    Tests isolated Sessions
    '''
    def setUp(self):

        self.USERS = USERS
        self.SWIPES = SWIPES
        self.SWIPE_TYPES = SWIPE_TYPES

        dict_to_database(UserSerializer,self.USERS)
        dict_to_database(SwipeSerializer,self.SWIPES)

    def test_session_duration_methods(self):
        for session in Session.objects.all():
            self.assertEqual(
                    session.session_duration(),
                    session.session_duration_overall() - session.breaks_duration()
            )
    def test_number_of_breaks_method(self):
        for session in Session.objects.all():
            self.assertEqual(
                    session.num_of_breaks(),
                    self.SWIPE_TYPES.count("FBR")
            )



    def test_NAT_value_of_opened_session_is_updated_overtime_if_IN_swipe_is_corrected(self):
        user1 = UserFactory()
        swipe1 = SwipeFactory(user = user1, swipe_type = "IN")        
        
        swipe2 = SwipeFactory( # correction of swipe1
                user = user1,
                swipe_type = "IN",
                correction_of_swipe = swipe1,
                datetime = swipe1.datetime + timedelta(seconds = 1),
        )

        nat_1 = swipe2.session.get_not_assigned_duration()
        sleep(1) # sleep creates needed time difference (better method?)
        nat_2 = swipe2.session.get_not_assigned_duration()

        self.assertNotEqual(nat_1, nat_2)    
        
    def create_swipe_new_swipe_with_time_offset(self, session, offset_hours, swipe_type):
        """
        For testing purposes, returns  new_swipe, original_swipe tupple
        """
        original_swipe = session.swipe_set.get(swipe_type = swipe_type)
        new_swipe = Swipe.objects.create(
                user = original_swipe.user,
                datetime = original_swipe.datetime + timedelta(hours=offset_hours),
                swipe_type = swipe_type,
                correction_of_swipe = original_swipe)
        return new_swipe,original_swipe

    def test_only_one_in_swipe_in_opened_session(self):
        s1 = Swipe.objects.create(user = User.objects.get(id= 1),
                datetime = timezone.now() + timedelta(hours=50),
                swipe_type = "IN")
        original_session = s1.session
        self.assertTrue(s1.session)
        s2 = Swipe.objects.create(user = User.objects.get(id= 1),
                datetime = timezone.now() + timedelta(hours=60),
                swipe_type = "IN",
                correction_of_swipe = s1)

        self.assertEqual(original_session.swipe_set.filter(swipe_type = "IN").count(), 1)

    def test_only_one_in_swipe_in_closed_session(self):
        session = Session.objects.get(id = 1)
        self.create_swipe_new_swipe_with_time_offset(session,50,"IN")
        self.assertEqual(session.swipe_set.filter(swipe_type = "IN").count(), 1)

    def test_only_one_swipe_out_closed_session(self):
        session = Session.objects.get(id = 2)
        self.create_swipe_new_swipe_with_time_offset(session,-1,"OUT")
        self.assertEqual(session.swipe_set.filter(swipe_type = "OUT").count(), 1)

    def test_session_duration_is_recalculated_for_correcting_swipe(self):
        session = Session.objects.get(id = 1)
        self.create_swipe_new_swipe_with_time_offset(session,-1,"OUT")
        self.assertEqual(session.duration, session.session_duration())

    def test_is_at_work(self):
        #not implemented function yet
        pass

    def test_get_date(self):
        session = Session.objects.get(id = 1)
        swipe = Swipe.objects.get(id = 1)

        self.assertEqual(swipe.swipe_type, "IN")
        self.assertEqual(session, swipe.session)
        self.assertEqual("<class 'datetime.datetime'>", str(type(session.get_date())))
        self.assertEqual(session.get_date(), swipe.datetime)

    def test_session_is_marked_as_modified(self):
        swipe = Swipe.objects.get(id = 1)
        self.assertFalse(swipe.session.modified)
        Swipe.objects.create(
                user = swipe.user,
                datetime = swipe.datetime - timedelta(hours = 1),
                swipe_type = swipe.swipe_type,
                correction_of_swipe = swipe
        )
        self.assertTrue(swipe.session.modified)

    def test_get_sessions_this_month(self):
        pass

    def test_get_not_work_duration(self):
        project1 = ProjectFactory(private=True)
        project2 = ProjectFactory(private=False)
        session1 = Session.objects.get(pk=1)
        session2 = Session.objects.get(pk=2)
        time1 = timedelta(hours=2)
        time2 = session2.get_not_assigned_duration()
        
        ProjectSeparationFactory(
            time_spend=time1, 
            session=session1,
            project=project1
        )
        ProjectSeparationFactory(
            time_spend=time2, 
            session=session2,
            project=project2
        )

        self.assertEqual(session1.get_not_work_duration(), time1)
        self.assertEqual(session2.get_not_work_duration(), timedelta(0))

class SwipeTestCase(TestCase):
    def setUp(self):

        self.USERS = USERS
        self.SWIPES = SWIPES
        self.SWIPE_TYPES = SWIPE_TYPES

        dict_to_database(UserSerializer,self.USERS)
        dict_to_database(SwipeSerializer,self.SWIPES)

    def test_swipes_cant_break_time_integrity(self):
        s1 = Swipe.objects.create(
                        id = 100,
                        user = User.objects.get(id= 1),
                        datetime = timezone.now() + timedelta(hours=150),
                        swipe_type = "IN"
                )
        self.assertTrue(Swipe.objects.all().filter(id = 100))
        try:
            s2 = Swipe.objects.create(
                    id = 101,
                    user = User.objects.get(id= 1),
                    datetime = timezone.now() + timedelta(hours=149),
                    swipe_type = "OUT"
            )
            self.fail("We cant write new swipe with less datetime")
        except ValueError:
            pass

        self.assertTrue(Swipe.objects.all().filter(id = 100))
        self.assertFalse(Swipe.objects.all().filter(id = 101))

    def test_allowed_types_returns_tupple(self):
        in_return = Swipe.objects.filter(swipe_type = "IN")[0].get_next_allowed_types()
        self.assertIn("tuple", str(type(in_return)))
        in_return = Swipe.objects.filter(swipe_type = "OUT")[0].get_next_allowed_types()
        self.assertIn("tuple", str(type(in_return)))

    def test_cant_break_swipes_integrity(self):
        """
        Only some sequences of swipes are allowed (IN after IN is not allowed
        and so on)
        """
        def create_swipe(type, offset, id):
            return Swipe.objects.create(
                    id = id,
                    user = User.objects.get(id= 1),
                    datetime = timezone.now() + timedelta(hours=offset),
                    swipe_type = type
            )
        #we are testing swipes if every last swipe in tupple exists
        SWIPE_SEQUENCE = [
                ("IN","IN",),
                ("OBR", "OBR",),
                ("FBR", "FBR",),
                ("OTR", "OTR",),
                ("FTR", "FTR",),
                ("OUT", "OUT",),
                ("FTR",),
                ("FBR",),
                ("IN","FTR",),
                ("FBR",),
        ]

        offset, id = 50, 50

        for tuple_assert in SWIPE_SEQUENCE:
            try:
                for swipe_type in tuple_assert:
                    create_swipe(swipe_type, offset, id)
                    offset, id = offset + 1, id + 1
                self.fail("It should be imposible to write this swipe_type")
            except ValueError:
                pass
            self.assertFalse(Swipe.objects.filter(id = id))

        user1 = UserFactory()
        swipe1 = SwipeFactory(user = user1, swipe_type = "IN")
        swipe2 = SwipeFactory(user = user1, swipe_type = "OUT")
        swipe3 = SwipeFactory(
                user = user1,
                swipe_type = "IN",
                correction_of_swipe = swipe1,
                datetime = swipe1.datetime - timedelta(seconds = 1),
        )
        #this should be posiible because last swipe is correction
        swipe4 = SwipeFactory(user = user1, swipe_type = "IN")


    def test_get_swipe_before(self):
        self.assertFalse(Swipe.objects.get(id = 1).get_last_swipe_same_user())
        self.assertEqual(1,Swipe.objects.get(id = 2).get_last_swipe_same_user().id)
        user1, user2 = UserFactory(), UserFactory()

        swipe1 = SwipeFactory(swipe_type = "IN", user = user1)
        swipe2 = SwipeFactory(swipe_type = "IN", user = user2)
        swipe3 = SwipeFactory(swipe_type = "OUT", user = user1)
        swipe4 = SwipeFactory(swipe_type = "OBR", user = user2)
        swipe5 = SwipeFactory(swipe_type = "OBR", user = user2, correction_of_swipe = swipe4)
        swipe7 = SwipeFactory(swipe_type = "FBR", user = user2)
        swipe8 = SwipeFactory(swipe_type = "OUT", user = user2)

        self.assertFalse(swipe1.get_last_swipe_same_user())
        self.assertFalse(swipe2.get_last_swipe_same_user())
        self.assertEqual(swipe5.id, swipe7.get_last_swipe_same_user().id)
        self.assertEqual(swipe1.id, swipe3.get_last_swipe_same_user().id)

        #testing swipe after so we dont have to repeat initialization
        self.assertEqual(swipe5.id, swipe2.get_next_swipe_same_user().id)

    def test_get_swipe_after(self):
        count = Swipe.objects.filter(user__username = "ondrej.vicar").count()
        self.assertFalse(Swipe.objects.get(id = count).get_next_swipe_same_user())
        self.assertEqual(8,Swipe.objects.get(id = 7).get_next_swipe_same_user().id)
        self.assertEqual(3,Swipe.objects.get(id = 2).get_next_swipe_same_user().id)

class ViewTestCase(TestCase):

    def test_home_page_redirects_to_login(self):
        client = Client()
        response = client.get(reverse("home"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/login/?next=/")

    def test_resolve_session_month(self):
        match = resolve("/sessions/bla.bla/2015/05/")
        self.assertEqual(match.kwargs["username"],"bla.bla")
        self.assertEqual(match.kwargs["year"],"2015")
        self.assertEqual(match.kwargs["month"],"05")

class TimeTestCase(TestCase):

    def test_app_time_is_same_as_server_time(self):
        server_now = datetime.now(pytz.utc)
        django_now = timezone.now()
        server_now = server_now.replace(microsecond = 0)
        django_now = django_now.replace(microsecond = 0)

        self.assertEqual(server_now, django_now)

class FormTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.swipe1 = SwipeFactory(user = self.user, swipe_type = "IN")
        self.swipe2 = SwipeFactory(user = self.user, swipe_type = "OUT")

    def test_swipe_edit_form(self):
        form_data = {"datetime": timezone.now()}

        form = SwipeEditForm(data = form_data, instance = self.swipe2)

        self.assertTrue(form.is_valid())

        form_data["datetime"] -= timedelta(seconds = 1)
        form = SwipeEditForm(data = form_data, instance = self.swipe2)

        self.assertFalse(form.is_valid())

        swipe = SwipeFactory(user = self.user, swipe_type = "IN")

        form_data["datetime"] += timedelta(hours = 1)
        form = SwipeEditForm(data = form_data, instance = self.swipe2)

        self.assertFalse(form.is_valid())

    def test_project_separation_form(self):
        #implement
        pass


class UtilsTestCase(TestCase):
    def test_num_of_elapsed_workdays(self):
        f = get_num_of_elapsed_workdays_in_month
        self.assertEqual(f(date(2016, 11, 1)), 0)
        self.assertEqual(f(date(2016, 11, 2)), 1)
        self.assertEqual(f(date(2016, 11, 3)), 2)
        self.assertEqual(f(date(2016, 11, 30)), 20)
        self.assertEqual(f(date(2017, 1, 1)), 0)
        self.assertEqual(f(date(2017, 1, 2)), 0)
        self.assertEqual(f(date(2017, 1, 3)), 1)

    
    def test_last_month(self):
        self.assertEqual(last_month(12),11)    
        self.assertEqual(last_month(1),12)
      
   
    def test_daily_hours(self):
        self.assertEqual(daily_hours(25),24) 
        self.assertEqual(daily_hours(2),2)
        self.assertEqual(daily_hours(0),0)
        self.assertEqual(daily_hours(24),24)
        self.assertEqual(daily_hours(-10),0)


class ManagersTestCase(TestCase):
    def test_number_work_hours_after_year(self):
        self.user = UserFactory()
        base_datetime = timezone.now() - timedelta(days=365)
        self.swipe1 = SwipeFactory(user=self.user, swipe_type="IN", datetime=base_datetime)
        self.swipe2 = SwipeFactory(user=self.user, swipe_type="OUT", datetime=base_datetime + timedelta(hours=1))
        self.assertEqual(0, Session.objects.get_hours_this_month(self.user), "Should have 0 hours")

        self.swipe1 = SwipeFactory(user=self.user, swipe_type="IN")
        self.swipe2 = SwipeFactory(user=self.user, swipe_type="OUT", datetime=timezone.now() + timedelta(hours=1))
        self.assertEqual(1, Session.objects.get_hours_this_month(self.user))
