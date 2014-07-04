# -*- coding: utf-8 -*-

from django.conf.urls import url
from salary import views

urlpatterns = [
    url(r'^$', views.index, name='salary_index'),
    url(r'^new/$', views.create, name='salary_create'),
    url(r'^(\d+)/pass/$', views.verify, name='salary_pass'),
    url(r'^(\d+)/deny/$', views.deny, name='salary_deny'),
]
