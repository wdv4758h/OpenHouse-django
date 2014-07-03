# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.vary import vary_on_headers

from wagtail.wagtailadmin.forms import SearchForm
from hrdb.forms import HrdbForm
from hrdb.models import Hrdb

hrdb_fields = ('department', 'grade', 'studentid', 'project', 'thesis', 'teacher', 'intern', 'nsc_project', 'language_ability', 'email', 'ip', 'create_time', 'update_time')

@vary_on_headers('X-Requested-With')
def hrdb_view(request):
    Model = Hrdb
    q = None
    p = request.GET.get("p", 1)
    is_searching = False

    if 'q' in request.GET:
        form = SearchForm(request.GET, placeholder="搜尋人才庫")
        if form.is_valid():
            q = form.cleaned_data['q']

            is_searching = True
            students = Model.objects.filter(
                Q(department__icontains=q) |
                Q(grade__icontains=q) |
                Q(project__icontains=q) |
                Q(thesis__icontains=q) |
                Q(teacher__icontains=q) |
                Q(intern__icontains=q) |
                Q(nsc_project__icontains=q) |
                Q(language_ability__icontains=q) |
                Q(email__icontains=q) |
                Q(update_time__icontains=q)
            )


    else:
        form = SearchForm(placeholder="搜尋人才庫")

    if not is_searching:
        students = Model.objects.all()

    if 'ordering' in request.GET:
        ordering = request.GET['ordering']

        if ordering in hrdb_fields:
            if ordering != 'id':
                students = students.order_by(ordering)
    else:
        ordering = 'id'

    total = len(students)
    paginator = Paginator(students, 20)

    try:
        students = paginator.page(p)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request, "company/hrdb_results.html", {
            'students': students,
            'is_searching': is_searching,
            'query_string': q,
            'ordering': ordering,
            'total': total,
        })
    else:
        return render(request, "company/hrdb.html", {
            'search_form': form,
            'students': students,
            'is_searching': is_searching,
            'ordering': ordering,
            'query_string': q,
            'total': total,
        })
