from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html', 'redirect_field_name' : 'login'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login'}, name='logout'),
)
