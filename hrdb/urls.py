from django.conf.urls import patterns, url
from hrdb import views

urlpatterns = patterns('',
    url('admin/', 'hrdb.views.hrdb_list', name='hrdb_admin'),
)
