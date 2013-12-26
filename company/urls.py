from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'register', 'company.views.register', name='company_register'),
    url(r'chpass', 'company.views.chpass', name='company_chpass'),
    url(r'view/(\d+)', 'company.views.view', name='company_view'),
    url(r'', 'company.views.list', name='company'),
)
