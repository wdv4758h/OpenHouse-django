from django.conf.urls import patterns, url
from hrdb import views

urlpatterns = patterns('',
    url('create', views.HrdbCreate.as_view(), name='hrdb_create'),
    url('admin/', 'hrdb.views.hrdb_list', name='hrdb_admin'),
)
