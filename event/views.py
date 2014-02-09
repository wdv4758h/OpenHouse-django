# _*_ coding: utf-8 _*_

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from company.models import Company

@login_required(redirect_field_name='index')
def dashboard(request):
    companys = Company.objects.all()
    return render_to_response('dashboard.html', {'companys': companys}, context_instance=RequestContext(request))
