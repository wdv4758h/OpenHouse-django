# _*_ coding: utf8 _*_

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.vary import vary_on_headers

from wagtail.wagtailadmin.forms import SearchForm
from hrdb.forms import HrdbForm
from hrdb.models import Hrdb

fields = ('department', 'grade', 'studentid', 'project', 'thesis', 'teacher', 'intern', 'nsc_project', 'language_ability', 'email', 'ip', 'create_time', 'update_time')

Model = Hrdb

@vary_on_headers('X-Requested-With')
def index(request):
    q = None
    p = request.GET.get("p", 1)
    is_searching = False

    if 'q' in request.GET:
        form = SearchForm(request.GET, placeholder="搜尋人才庫")
        if form.is_valid():
            q = form.cleaned_data['q']

            is_searching = True
            students = Model.objects.filter(
                Q(name__icontains=q) |
                Q(department__icontains=q) |
                Q(grade__icontains=q) |
                Q(studentid__icontains=q) |
                Q(project__icontains=q) |
                Q(thesis__icontains=q) |
                Q(teacher__icontains=q) |
                Q(intern__icontains=q) |
                Q(nsc_project__icontains=q) |
                Q(language_ability__icontains=q) |
                Q(email__icontains=q) |
                Q(ip__icontains=q) |
                Q(create_time__icontains=q) |
                Q(update_time__icontains=q)
            )


    else:
        form = SearchForm(placeholder="搜尋人才庫")

    if not is_searching:
        students = Model.objects.all()

    if 'ordering' in request.GET:
        ordering = request.GET['ordering']

        if ordering in fields:
            if ordering != 'id':
                students = students.order_by(ordering)
    else:
        ordering = 'id'

    paginator = Paginator(students, 20)

    try:
        students = paginator.page(p)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request, "hrdb/results.html", {
            'students': students,
            'is_searching': is_searching,
            'query_string': q,
            'ordering': ordering,
        })
    else:
        return render(request, "hrdb/index.html", {
            'search_form': form,
            'students': students,
            'is_searching': is_searching,
            'ordering': ordering,
            'query_string': q,
        })

def create(request, create_only=False):
    if request.POST:
        ip = request.META.get('REMOTE_ADDR')
        form = HrdbForm(request.POST)
        if form.is_valid():
            student = form.save(ip=ip)
            messages.success(request, "人才庫: '{0}' 已建立.".format(student))
            return redirect('hrdb_index')
        else:
            messages.error(request, "有錯誤，無法建立" )
    else:
        form = HrdbForm()

    if create_only:
        return form
    else:
        return render(request, 'hrdb/create.html', {
            'form': form,
        })

def edit(request, user_id):
    student = get_object_or_404(Model, id=user_id)
    if request.POST:
        form = HrdbForm(request.POST, instance=student)
        if form.is_valid():
            user = form.save()
            messages.success(request, "人才庫: '{0}' 已更新.".format(student))
            return redirect('hrdb_index')
        else:
            messages.error(request, "有錯誤，無法更新" )
    else:
        form = HrdbForm(instance=student)

    return render(request, 'hrdb/edit.html', {
        'student': student,
        'form': form,
    })
