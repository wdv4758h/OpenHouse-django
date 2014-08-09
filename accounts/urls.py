from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^login[/]$', 'django.contrib.auth.views.login', {'template_name': 'login.html', 'redirect_field_name' : 'index'}, name='login'),
    url(r'^logout[/]$', 'django.contrib.auth.views.logout', {'next_page': settings.YEAR + '/'}, name='logout'),
    #url(r'^password$', 'django.contrib.auth.views.password_change', {'template_name': 'password_change.html', 'post_change_redirect': '/'}, name='password_change'),
)
