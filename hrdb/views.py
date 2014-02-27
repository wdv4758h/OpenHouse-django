# _*_ coding: utf8 _*_

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from hrdb.models import Hrdb

@login_required(redirect_field_name='index')
def hrdb_list(request):
    hrdb = Hrdb.objects.all()
    length = len(hrdb)
    categorys = ['序號', '姓名', '系所', '年級', '學號', '電子信箱', '建立時間', '更新時間']
    header = '管理交大人才庫資料'
    return render_to_response('hrdb_admin.html', {'header': header, 'items': hrdb, 'categorys': categorys, 'total': length}, context_instance=RequestContext(request))
