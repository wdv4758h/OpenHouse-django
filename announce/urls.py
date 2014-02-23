from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url('', 'announce.views.news', name='announce'),
)
