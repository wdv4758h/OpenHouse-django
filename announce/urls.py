from django.conf.urls import patterns, url
from announce import views

urlpatterns = patterns('',
    url(r'view/(?P<pk>\d+)', views.News.as_view(), name='announce_view'),
    url('', 'announce.views.news', name='announce'),
)
