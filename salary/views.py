# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.vary import vary_on_headers

from wagtail.wagtailadmin.forms import SearchForm
from salary.forms import SalaryForm
from salary.models import Salary

Model = Salary

@vary_on_headers('X-Requested-With')
def index(request):
    q = None
    p = request.GET.get("p", 1)
    is_searching = False

    if 'q' in request.GET:
        form = SearchForm(request.GET, placeholder="搜尋報帳")
        if form.is_valid():
            q = form.cleaned_data['q']

            is_searching = True
            salary = Model.objects.filter(
                Q(staff__studentid__icontains=q) |
                Q(staff__name__icontains=q) |
                Q(staff__email__icontains=q) |
                Q(start__icontains=q) |
                Q(end__icontains=q) |
                Q(desc__icontains=q) |
                Q(status__icontains=q)
            )
    else:
        form = SearchForm(placeholder="搜尋報帳")

    if not is_searching:
        salary = Model.objects.all()

    if 'ordering' in request.GET:
        ordering = request.GET['ordering']

        if ordering in ['id', 'staff', 'start', 'end']:
            if ordering != 'id':
                salary = salary.order_by(ordering)
    else:
        ordering = 'id'

    paginator = Paginator(salary, 20)

    try:
        salary = paginator.page(p)
    except PageNotAnInteger:
        salary = paginator.page(1)
    except EmptyPage:
        salary = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request, "salary/results.html", {
            'salary': salary,
            'is_searching': is_searching,
            'query_string': q,
            'ordering': ordering,
        })
    else:
        return render(request, "salary/index.html", {
            'search_form': form,
            'salary': salary,
            'is_searching': is_searching,
            'ordering': ordering,
            'query_string': q,
        })

def create(request):
    if request.POST:
        form = SalaryForm(request.POST)
        if form.is_valid():
            salary = form.save()
            messages.success(request, "報帳 '{0}' 已建立.".format(salary))
            return redirect('salary_index')
        else:
            messages.error(request, "報帳有錯誤，無法建立" )
    else:
        form = SalaryForm()

    return render(request, 'salary/create.html', {
        'form': form,
    })
