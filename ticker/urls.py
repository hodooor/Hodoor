from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from attendance import views
from django.contrib.auth.views import (
    logout,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete
)
from rest_framework import routers

swipes_router = routers.DefaultRouter()
swipes_router.register(r'api/swipes', views.SwipeViewSet)

keys_router = routers.DefaultRouter()
keys_router.register(r'api/keys', views.KeyViewSet)


urlpatterns = [
    #  /
    url(r'^$', views.home_page, name='home'),

    # /admin/
    url(r'^admin/', admin.site.urls),

    # /api/swipes/
    url(r'^', include(swipes_router.urls)),
    # /api/keys/
    url(r'^', include(keys_router.urls)),

    # /plate/
    url(r'^plate/', include('django_spaghetti.urls')),

    url(r'^logout/$', logout, {'next_page': '/login/'}),

    # /login/  #/logout/ etc... https://docs.djangoproject.com/ja/1.9/topics/auth/default/
    url(r'^', include('django.contrib.auth.urls')),

    # /user/username/
    url(r'^user/(?P<username>[\w.@+-]+)/$', views.user, name='user'),

    url(r'^sessions/(?P<username>[\w.@+-]+)/$', views.sessions, name='sessions'),
    # /sessions/username/

    # /sessions/username/2015/05
    url(r'^sessions/(?P<username>[\w.@+-]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
        views.sessions_month,
        name='sessions_month'),

    # /sessions/username/id1
    # /sessions/username/id354
    url(r'^sessions/(?P<username>[\w.@+-]+)/id(?P<id>\d+)/$',
        views.session_detail,
        name='session_detail'),
        
    url(r'^swipes/(?P<username>[\w.@+-]+)/id(?P<id>\d+)/$',
        views.swipe_detail,
        name='swipe_detail'),
    # /swipes/username/
    url(r'^swipes/(?P<username>[\w.@+-]+)/$', views.swipes, name='swipes'),

    # password reset section
    url(r'^user/password/reset/$',
        password_reset,
        {'post_reset_redirect': '/user/password/reset/done/'},
        name="password_reset"),

    url(r'^user/password/reset/done/$', password_reset_done),

    url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {'post_reset_redirect' : '/user/password/done/'}),

    url(r'^user/password/done/$',
        password_reset_complete),

     # /administrator/2016/09
    url(r'^administrator/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<project>[\w.@+-]+)$',
        views.administrator,
        name='administrator'),
    url(r'^administrator/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
        views.administrator,
        name='administrator'),
    url(r'^administrator/$',
        views.administrator,
        name='default_administrator'),
    
    # /h_request/username/
    url(r'^h_request/(?P<username>[\w.@+-]+)/$',
        views.holidays_request,
        name='h_request'),
    
    # /h_verification/username/id1/
    url(r'^h_verification/(?P<username>[\w.@+-]+)/id(?P<id>\d+)/$',
        views.holidays_verification,
        name='h_verification'),

   # /generate/pdf/username/2017/7
    url(r'^generate/pdf/(?P<username>[\w.@+-]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
        views.generate_pdf,
       name='work_report_pdf'),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
