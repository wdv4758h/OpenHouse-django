from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'', 'company.views.list', name='company'),
)
