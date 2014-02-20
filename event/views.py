# _*_ coding: utf-8 _*_

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from company.models import Company

@login_required(redirect_field_name='index')
def dashboard(request, event):
    companys = Company.objects.all()
    return render_to_response('table/dashboard.html', {'companys': companys, 'event_url': event}, context_instance=RequestContext(request))

@login_required(redirect_field_name='index')
def event_list(request, event, list_name):
    companys = Company.objects.all()
    return render_to_response('table/%s.html' % list_name, {'companys': companys, 'event_url': event}, context_instance=RequestContext(request))

@login_required(redirect_field_name='index')
def view(request, num, event):
    company = Company.objects.filter(cid=num)[0]
    return render_to_response('table/event_per_company_status.html', {'company': company, 'eventname': event}, context_instance=RequestContext(request))
