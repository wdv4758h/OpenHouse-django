from django.conf.urls import url
from company import views

urlpatterns = [
    url(r'^$', views.index, name='company_index'),
    url(r'^new/$', views.create, name='company_create'),
    url(r'^(\d+)/$', views.edit, name='company_edit'),
]
