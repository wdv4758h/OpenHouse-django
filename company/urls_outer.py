# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from company.views_outer import hrdb_view, company_edit

urlpatterns = [
    url(r'^hrdb/', hrdb_view, name='company_hrdb'),
    url(r'^view/', login_required(TemplateView.as_view(template_name='company/view.html')), name='company_view'),
    url(r'^edit/', company_edit, name='company_edit'),
]
