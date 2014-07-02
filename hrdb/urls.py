from django.conf.urls import url
from hrdb import views

urlpatterns = [
    url(r'^$', views.index, name='hrdb_index'),
    url(r'^new/$', views.create, name='hrdb_create'),
    url(r'^(\d+)/$', views.edit, name='hrdb_edit'),
]
