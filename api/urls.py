# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=True)

urlpatterns = patterns('',
    url('(?P<year>\d{4})/news', views.NewsViewSet.as_view()),
    url(r'^', include(router.urls)),
)
