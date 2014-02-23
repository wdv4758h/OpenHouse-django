# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('resume', views.SalaryViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
