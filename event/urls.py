# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url('dashboard$', 'event.views.dashboard', name='dashboard'),
    url(r'view/(\d+)', 'event.views.view', name='event_view'),
    url('activity$', 'event.views.event_list', {'list_name': 'activity'}, name='activity'),
    url('sponsor$', 'event.views.event_list', {'list_name': 'sponsor'}, name='sponsor'),
    url('stuvote$', 'event.views.event_list', {'list_name': 'vote'}, name='vote'),
    url('teach$', 'event.views.event_list', {'list_name': 'teach'}, name='teach'),
    url('visit$', 'event.views.event_list', {'list_name': 'visit'}, name='visit'),
    url('forum/info$', 'event.views.event_list', {'list_name': 'forum_info'}, name='visit'),
)
