"""ticker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin


from attendance import views

from rest_framework import routers

swipes_router = routers.DefaultRouter()
swipes_router.register(r'api/swipes', views.SwipeViewSet)

keys_router = routers.DefaultRouter()
keys_router.register(r'api/keys',views.KeyViewSet)


urlpatterns = [
	#/
    url(r'^$', views.home_page, name ='home'),
    
    #/admin/
    url(r'^admin/', admin.site.urls),
    
    #/api/swipes/
    url(r'^', include(swipes_router.urls)),
    #/api/keys/
    url(r'^', include(keys_router.urls)), 
    
    #/plate/
    url(r'^plate/', include('django_spaghetti.urls')),

    url(r'^logout/$', 'django.contrib.auth.views.logout',
    {'next_page': '/login/'}),

    #/login/  #/logout/ etc... https://docs.djangoproject.com/ja/1.9/topics/auth/default/
    url(r'^', include('django.contrib.auth.urls')),
    
    #/user/username/
    url(r'^user/(?P<username>[\w.@+-]+)/$', views.user, name='user'),
    
    #/sessions/username/
    url(r'^sessions/(?P<username>[\w.@+-]+)/$', views.sessions, name='sessions'),
    #/swipes/username/
    url(r'^swipes/(?P<username>[\w.@+-]+)/$', views.swipes, name='swipes'),
]   
