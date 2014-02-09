# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url('dashboard$', 'event.views.dashboard', name='dashboard'),
)
