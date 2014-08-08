from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.views.decorators.vary import vary_on_headers

from wagtail.wagtailadmin.forms import SearchForm
from company.forms import CompanyCreationForm as UserCreationForm, CompanyEditForm as UserEditForm
from wagtail.wagtailcore.compat import AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME

from company.models import Company

User = Company

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
        form = SearchForm(request.GET, placeholder=_("Search users"))
        if form.is_valid():
            q = form.cleaned_data['q']

            is_searching = True
            users = User.objects.filter(
                Q(cid__icontains=q) |
                Q(shortname__icontains=q) |
                Q(name__icontains=q) |
                Q(category__icontains=q) |
                Q(hr_email__icontains=q) |
                Q(hr_phone__icontains=q) |
                Q(hr_mobile__icontains=q) |
                Q(hr_email__icontains=q)
            )
    else:
        form = SearchForm(placeholder=_("Search users"))

    if not is_searching:
        users = User.objects

    users = users.order_by('cid')

    if 'ordering' in request.GET:
        ordering = request.GET['ordering']

        if ordering in ['name', 'cid']:
            if ordering != 'cid':
                users = users.order_by(ordering)
    else:
        ordering = 'cid'

    paginator = Paginator(users, 20)

    try:
        users = paginator.page(p)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request, "company/results.html", {
            'users': users,
            'is_searching': is_searching,
            'query_string': q,
            'ordering': ordering,
        })
    else:
        return render(request, "company/index.html", {
            'search_form': form,
            'users': users,
            'is_searching': is_searching,
            'ordering': ordering,
            'query_string': q,
        })

@permission_required(change_user_perm)
def create(request):
    if request.POST:
        # Company has logo which is ImageField,
        # need pass in request.FILES
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, _("User '{0}' created.").format(user))
            return redirect('company_index')
        else:
            messages.error(request, _("The user could not be created due to errors.") )
    else:
        form = UserCreationForm()

    return render(request, 'company/create.html', {
        'form': form,
    })


@permission_required(change_user_perm)
def edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.POST:
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, _("User '{0}' updated.").format(user))
            return redirect('company_index')
        else:
            messages.error(request, _("The user could not be saved due to errors."))
    else:
        form = UserEditForm(instance=user)

    return render(request, 'company/edit.html', {
        'user': user,
        'form': form,
    })
