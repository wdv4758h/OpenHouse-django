# _*_ coding: utf-8 _*_

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from company.models import Company

import glob

@login_required(redirect_field_name='index')
def list(request):
    companys = Company.objects.all()
    return render_to_response('company.html', {'companys': companys}, context_instance=RequestContext(request))
@login_required(redirect_field_name='index')
def view(request, num):
    company = Company.objects.filter(cid=num)[0]

    try:
        img_name = glob.glob1('static/images/company_logo/', company.cid + '-' + company.shortname + '.*')[0].split('/')[-1]
    except:
        img_name = ""

    name = company.shortname

    field_names = [ '統編', '公司名稱', '公司簡稱', '類別', '公司電話', '公司地址', '公司網站', '公司簡介', '公司介紹', '人資姓名', '人資電話', '人資傳真', '人資手機', '人資信箱', '更新時間']

    company = [ company.cid, company.name, company.shortname, company.category, company.phone, company.address, company.website, company.brief, company.introduction, company.hr_name, company.hr_phone, company.hr_fax, company.hr_mobile, company.hr_email, company.timestamp ]

    company = zip(field_names, company)

    return render_to_response('company_view.html', {'company': company, 'name': name, 'img': img_name}, context_instance=RequestContext(request))
