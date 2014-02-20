from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'register', 'company.views.register', name='company_register'),
    url(r'chpass', 'company.views.chpass', name='company_chpass'),
    url(r'view/(\d+)', 'company.views.view', name='company_view'),
    url(r'update/(?P<pk>\d+)', views.CompanyUpdate.as_view(), name='company_update'),
    url(r'', 'company.views.list', name='company'),
)
