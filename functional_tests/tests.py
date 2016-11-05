from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from attendance.models import Key, Swipe, Session
from attendance.factories import UserFactory, SwipeFactory

from rest_framework import status
import sys
import re
from rest_framework.test import APIClient
from unittest import skip
from rest_framework.authtoken.models import Token

from django.contrib.auth.hashers import check_password
from selenium.common.exceptions import NoSuchElementException
from django.utils import timezone
from datetime import timedelta, datetime
import time

from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.conf import settings
User = get_user_model()
from .server_tools import reset_database, create_session_on_server

from .management.commands.create_session import create_pre_authenticated_session
from django.test.utils import override_settings
from django.conf import settings

class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.browser = webdriver.Firefox()
                cls.browser.implicitly_wait(3)
                cls.server_user, cls.server_host = arg.split('=')[1].split('@')
                print("server host: " + cls.server_host )
                print("server user: " + cls.server_user )
                cls.server_url = 'http://' + cls.server_host
                print("server url: " + cls.server_url )
                cls.against_staging = True
                return
        super(FunctionalTest, cls).setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        if not cls.against_staging:
            super(FunctionalTest, cls).tearDownClass()

    def setUp(self):
        if self.against_staging:
            reset_database(self.server_host)

    def login_by_form(self, usr, pswd, webdriver):
        username = webdriver.find_element_by_id("id_username")
        password = webdriver.find_element_by_id("id_password")

        username.send_keys(usr)
        password.send_keys(pswd)

        webdriver.find_element_by_css_selector("input[type='submit']").click()


    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout = 30).until(
                lambda b: b.find_element_by_id(element_id),
                "Could not find element with id {}. Page text was:\n{}".format(
                element_id, self.browser.find_element_by_tag_name("body").text
                )
        )

    def wait_to_be_logged_in(self, username):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(username, navbar.text)

    def wait_to_be_logged_out(self, username):
        self.wait_for_element_with_id('id_login')
        self.assertIn("Login",
                self.browser.find_element_by_tag_name("body").text
        )

    def create_pre_authenticated_session(self, username):
        if self.against_staging:
            session_key = create_session_on_server(self.server_user +"@" +self.server_host, username)
        else:
            session_key = create_pre_authenticated_session(username)

        self.browser.add_cookie(dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path='/',
        ))

class LoginLogoutTest(FunctionalTest):
    def test_login_and_logut_users(self):

        user = UserFactory.build()
        self.browser.get(self.server_url)

        self.create_pre_authenticated_session(user.username)
        self.browser.get(self.server_url)

        sessions_header = self.browser.find_element_by_tag_name("h1").text
        self.wait_to_be_logged_in(user.username)
        self.assertIn("profile", sessions_header)
        self.assertEqual(self.server_url + "/user/" + user.username+ "/",self.browser.current_url)
        self.browser.find_element_by_class_name('a-logout').click()
        self.wait_to_be_logged_out(user.username)
        self.assertIn(self.server_url + "/login/",self.browser.current_url)

    def test_new_pre_auth(self):
        user = UserFactory.build()
        self.browser.get(self.server_url)
        self.wait_to_be_logged_out(user.username)

        print(user.username)
        self.create_pre_authenticated_session(user.username)

        self.browser.get(self.server_url)
        self.wait_to_be_logged_in(user.username)
class LayoutStylingTest(FunctionalTest):

    def test_admin_layout_and_styling(self):
        self.browser.get(self.server_url+"/admin/")
        self.browser.set_window_size(1024, 768)

        color = self.browser.find_element_by_id("header").value_of_css_property('background-color')

        self.assertEqual(color, "rgba(65, 118, 144, 1)")

class PageNavigationTest(FunctionalTest):

    def test_click_on_logo_returns_home_page(self):

        user = UserFactory.create()

        #logged out - just refreshing page
        self.browser.get(self.server_url)
        self.browser.find_element_by_class_name('navbar-brand').click()
        self.assertEqual(
                self.server_url + "/login/?next=/",
                self.browser.current_url
        )

        #login - logo taking us to profile page
        self.login_by_form(user.username,"password", self.browser)
        self.assertEqual(
                self.server_url + "/user/" + user.username + "/",
                self.browser.current_url
        )
        self.browser.find_element_by_class_name('navbar-brand').click()
        self.assertEqual(
                self.server_url + "/user/" + user.username + "/",
                self.browser.current_url
        )
        self.browser.find_element_by_class_name('a-logout').click()
        self.assertIn(self.server_url + "/login/",self.browser.current_url)

    def test_click_on_logout(self):

        user = UserFactory.create()
        self.login_by_form(user.username,"password", self.browser)
        self.assertEqual(
                self.server_url + "/user/" + user.username + "/",
                self.browser.current_url
        )
        self.browser.find_element_by_class_name('a-logout').click()
        self.assertIn(self.server_url + "/login/",self.browser.current_url)


    def test_click_on_sessions(self):
        user = UserFactory.create()
        self.login_by_form(user.username,"password", self.browser)
        self.browser.find_element_by_class_name('a-sessions').click()

        self.assertIn(
                self.server_url + "/sessions/" + user.username + "/",
                self.browser.current_url
        )
        self.browser.find_element_by_class_name('a-logout').click()
        self.assertIn(self.server_url + "/login/",self.browser.current_url)

    def test_click_on_swipes(self):
        user = UserFactory.create()

        self.login_by_form(user.username,"password", self.browser)
        self.browser.find_element_by_class_name('a-swipes').click()

        self.assertEqual(
                self.server_url + "/swipes/" + user.username + "/",
                self.browser.current_url
        )
        self.browser.find_element_by_class_name('a-logout').click()
        self.assertIn(self.server_url + "/login/",self.browser.current_url)


class PageAccessTest(FunctionalTest):
    def test_user_cant_access_another_profile(self):
        user1 = UserFactory.create()
        user2 = UserFactory.create()
        self.browser.get(self.server_url)
        self.login_by_form(user1.username,"password", self.browser)
        self.browser.get(self.server_url + "/sessions/" + user2.username + "/")
        self.assertIn("Restricted", self.browser.page_source, 1)
        self.browser.get(self.server_url + "/swipes/" + user2.username + "/")
        self.assertIn("Restricted", self.browser.page_source, 2)
        self.browser.get(self.server_url + "/user/" + user2.username + "/")
        self.assertIn("Restricted", self.browser.page_source, 3)
        self.browser.get(self.server_url + "/logout/")
        self.assertIn(self.server_url + "/login/",self.browser.current_url)

    def test_admin_can_access_another_profile(self):
        user1 = UserFactory.create(
                first_name = "Fratišek",
                last_name= "Vičar",
                is_staff = True,
        )
        user2 = UserFactory.create()
        self.browser.get(self.server_url)
        self.login_by_form(user1.username,"password", self.browser)
        self.browser.get(self.server_url + "/user/" + user2.username + "/")
        self.assertIn("Hours", self.browser.page_source)


class SessionTest(FunctionalTest):
    def test_there_should_be_no_session_long_time_ago(self):

        user = UserFactory.create()
        swipe = SwipeFactory(user = user, swipe_type = "IN")
        self.browser.get(self.server_url)
        self.login_by_form(user.username,"password", self.browser)
        self.assertEqual(Session.objects.count(), 1)
        SESSION_URL = self.server_url + "/sessions/" + user.username + "/2014/06/"

        self.browser.get(SESSION_URL)
        self.assertEqual(SESSION_URL,self.browser.current_url)
        try:
            element = self.browser.find_element_by_link_text("Detail")
        except NoSuchElementException:
            pass
        else:
            self.fail("There are sessions!")
        finally:
            self.browser.get(self.server_url + "/logout/")
            self.assertIn(self.server_url + "/login/",self.browser.current_url)

    def test_user_can_look_up_his_sessions_months(self):
        user = UserFactory.create()


        swipe = SwipeFactory(
                user = user,
                swipe_type = "IN",
                datetime = timezone.now() - timedelta(hours = 24*32))
        swipe = SwipeFactory(
                user = user,
                swipe_type = "OUT",
                datetime = timezone.now() - timedelta(hours = 24*31))
        swipe = SwipeFactory(
                user = user,
                swipe_type = "IN",
                datetime = timezone.now() + timedelta(hours = 1))
        swipe = SwipeFactory(
                user = user,
                swipe_type = "OUT",
                datetime = timezone.now() + timedelta(hours = 2))
        swipe = SwipeFactory(
                user = user,
                swipe_type = "IN",
                datetime = timezone.now() + timedelta(hours = 24*31))
        swipe = SwipeFactory(
                user = user,
                swipe_type = "OUT",
                datetime = timezone.now() + timedelta(hours = 24*32))
        self.assertEqual(Session.objects.count(), 3)
        for session in Session.objects.all():
            self.browser.get(self.server_url)
            self.login_by_form(user.username,"password", self.browser)
            session_url = "{0}/sessions/{1}/{2}/{3:0>2}/".format(
                    self.server_url,
                    user.username,
                    session.get_date().year,
                    session.get_date().month,
            )

            self.browser.get(session_url)
            try:
                self.browser.find_element_by_link_text("Detail")
            except NoSuchElementException:
                self.fail("Can't find Detail on page {}, session date: {}".format(
                        session_url,
                        session.get_date(),
                ))
            finally:
                self.browser.get(self.server_url + "/logout/")
                self.assertIn(self.server_url + "/login/",self.browser.current_url)

class APITest(FunctionalTest):
    '''
    Testing API for posting and receiving swipes - for clients
    '''
    def setUp(self):
        self.user = UserFactory.create()
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_keys_are_available(self):
        response = self.client.get("/api/keys/")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_swipes_are_available(self):
        response = self.client.get("/api/swipes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_swipe_can_be_posted(self):
        data = {"user": self.user.id, "swipe_type": "IN", "datetime":"2016-06-04T13:40Z"}
        response = self.client.post("/api/swipes/",data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
