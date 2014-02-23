# _*_ coding: utf8 _*_

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from announce.models import Announce

@login_required(redirect_field_name='index')
def news(request):
    news = Announce.objects.all()
    categorys = ['#', '標題', '發佈時間', '更新時間', '檢視']
    header = '最新訊息'
    return render_to_response('announce.html', {'header': header, 'items': news, 'categorys': categorys}, context_instance=RequestContext(request))
