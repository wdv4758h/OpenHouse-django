# _*_ coding: utf8 _*_

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from staff.models import Staff, Resume, Salary, SalaryForm

def list(request):
    staffs = Staff.objects.all()
    categorys = ['學號', '姓名', '職稱', '手機號碼', 'E-mail', 'OH BBS 帳號', '動作']
    header = '工作人員名單'
    return render_to_response('staff.html', {'header': header, 'items': staffs, 'categorys': categorys}, context_instance=RequestContext(request))

def salary_create(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            new_salary = form.save()
            return HttpResponseRedirect("/staffs/salary")
    else:
        form = SalaryForm()

    #add 'form-control' class and placeholder
    for field in form.fields.keys():
        field_obj = form.fields[field]

        field_obj.widget.attrs = {
                'class' : 'form-control',
                'placeholder' : field_obj.help_text}
        field_obj.help_text = ''

        #if field_obj.widget.attrs['name'] == 'start_time':
        #    field_obj.widget.attrs['type'] = 'datetime-local'

    return render_to_response('salary_create.html', {'form': form}, context_instance=RequestContext(request))

def salary_list(request):
    salarys = Salary.objects.all()
    return render_to_response('salary_list.html', {'salarys': salarys}, context_instance=RequestContext(request))

def staff_detail(request, num):
    staff = Staff.objects.filter(studentid=num)[0]
    preheader = '檢視工作人員 - '
    header = staff.name
    fields = ['學號', '姓名', '性別', '出生年月日', '職稱', '手機號碼', 'E-mail', 'FB個人首頁連結', 'BS2帳號', 'OH BBS帳號', '郵局帳號', '審核通過', '更新時間']

    staff = (staff.studentid, staff.name, staff.gender, staff.birthday, staff.role, staff.mobile, staff.email, staff.fb_url, staff.bs2id, staff.ohbbsid, staff.postacct, staff.verify, staff.timestamp)

    staff = zip(fields, staff)

    return render_to_response('detailview.html', {'preheader': preheader, 'header': header, 'data': staff}, context_instance=RequestContext(request))
