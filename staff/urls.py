from django.conf.urls import url
from staff import views

urlpatterns = [
    url(r'^$', views.index, name='staff_index'),
    url(r'^new/$', views.create, name='staff_create'),
    url(r'^(\d+)/$', views.edit, name='staff_edit'),
]
