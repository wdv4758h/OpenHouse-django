from django.conf.urls import patterns, url

#tmp
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url('docs', TemplateView.as_view(template_name="info.html"), name='docs'),
    url('salary$', 'staff.views.salary_list', name='salary_list'),
    url('salary/create', 'staff.views.salary_create', name='salary_create'),
    url(r'view/(.+)', 'staff.views.staff_detail', name='staff_view'),
    url('', 'staff.views.list', name='staff'),
)
