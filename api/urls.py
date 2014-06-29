# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=True)

inner_urls = patterns('',
    url('^news/', views.NewsList.as_view(), name='news-list'),
    url('', include(router.urls)),
)

urlpatterns = patterns('',
    #url(r'^(?P<year>\d{4})/', include(inner_urls)),
    url(r'^\d{4}/', include(inner_urls)),
)
