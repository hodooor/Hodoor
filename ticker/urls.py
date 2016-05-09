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

router = routers.DefaultRouter()
router.register(r'swipes', views.SwipeViewSet)

router2 = routers.DefaultRouter()
router.register(r'keys',views.KeyViewSet)


urlpatterns = [
    url(r'^$', views.home_page, name = 'home'),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^plate/', include('django_spaghetti.urls')), 
    url(r'^', include(router2.urls)), 
    url(r'^sessions/', views.sessions, name = "sessions"),
]   
