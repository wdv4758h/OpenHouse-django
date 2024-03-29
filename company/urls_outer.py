# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from company.views_outer import hrdb_view, company_edit, company_requirement_edit, company_event_status

urlpatterns = [
    url(r'^hrdb/$', hrdb_view, name='company_hrdb'),
    url(r'^view/$', login_required(TemplateView.as_view(template_name='company/view.html')), name='company_view'),
    url(r'^(rdss)/$', company_event_status, name='company_rdss'),
    url(r'^(rdss)/edit/', company_requirement_edit, name='company_rdss_edit'),
    url(r'^(recruit)/edit/', company_requirement_edit, name='company_recruit_edit'),
    url(r'^edit/', company_edit, name='company_edit'),
]
