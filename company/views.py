from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from company.models import Company

def list(request):
    companys = Company.objects.all()
    return render_to_response('company.html', {'companys': companys}, context_instance=RequestContext(request))
def view(request, num):
    company = Company.objects.filter(cid=num)[0]
    return render_to_response('company_view.html', {'company': company}, context_instance=RequestContext(request))
