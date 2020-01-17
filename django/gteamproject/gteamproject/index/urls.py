from django.conf.urls import url
from . import views

urlpattern = [
    url(r'^$', views.index_view)
]
