from django.conf.urls import url
from . import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    url(r'^user/$', views.users),
    url(r'^manager/$', csrf_exempt(views.manager)),
    url(r'^api/doc/$', get_swagger_view(title='Rest API DOC')),
    url(r'^$', views.home),
    url(r'^stadium/$', views.stadium),
    url(r'^api/push/$', csrf_exempt(views.post_call))
    ]