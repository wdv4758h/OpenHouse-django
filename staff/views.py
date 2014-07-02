# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.vary import vary_on_headers

from wagtail.wagtailadmin.forms import SearchForm
from staff.forms import StaffCreationForm as UserCreationForm, StaffEditForm as UserEditForm
from wagtail.wagtailcore.compat import AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME

from staff.models import Staff

User = Staff

# Typically we would check the permission 'auth.change_user' for user
# management actions, but this may vary according to the AUTH_USER_MODEL
# setting
change_user_perm = "{0}.change_{1}".format(AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME.lower())


@permission_required(change_user_perm)
@vary_on_headers('X-Requested-With')
def index(request):
    q = None
    p = request.GET.get("p", 1)
    is_searching = False

    if 'q' in request.GET:
        form = SearchForm(request.GET, placeholder="搜尋工作人員")
        if form.is_valid():
            q = form.cleaned_data['q']

            is_searching = True
            users = User.objects.filter(
                Q(studentid__icontains=q) |
                Q(name__icontains=q) |
                Q(email__icontains=q) |
                Q(mobile__icontains=q) |
                Q(ohbbsid__icontains=q)
            )
    else:
        form = SearchForm(placeholder="搜尋工作人員")

    if not is_searching:
        users = User.objects

    users = users.order_by('studentid')

    if 'ordering' in request.GET:
        ordering = request.GET['ordering']

        if ordering in ['name', 'studentid']:
            if ordering != 'studentid':
                users = users.order_by(ordering)
    else:
        ordering = 'studentid'

    paginator = Paginator(users, 20)

    try:
        users = paginator.page(p)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request, "staff/results.html", {
            'users': users,
            'is_searching': is_searching,
            'query_string': q,
            'ordering': ordering,
        })
    else:
        return render(request, "staff/index.html", {
            'search_form': form,
            'users': users,
            'is_searching': is_searching,
            'ordering': ordering,
            'query_string': q,
        })

@permission_required(change_user_perm)
def create(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "工作人員 '{0}' 已經建立".format(user))
            return redirect('staff_index')
        else:
            messages.error(request, "有錯誤，無法儲存")
    else:
        form = UserCreationForm()

    return render(request, 'staff/create.html', {
        'form': form,
    })


@permission_required(change_user_perm)
def edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.POST:
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, "工作人員 '{0}' 已更新".format(user))
            return redirect('staff_index')
        else:
            messages.error(request, "有錯誤，無法儲存")
    else:
        form = UserEditForm(instance=user)

    return render(request, 'staff/edit.html', {
        'user': user,
        'form': form,
    })
