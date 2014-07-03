# -*- coding: utf-8 -*-

from django.conf.urls import url
from company.views_outer import hrdb_view

urlpatterns = [
    url(r'^hrdb/', hrdb_view, name='company_hrdb'),
]
