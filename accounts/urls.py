from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^register/$', 'dt.accounts.views.register'),
    (r'^profile/$', 'dt.accounts.views.profile'),
    (r'^login/$', 'django.contrib.auth.views.login',
                  {'template_name': 'accounts/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
)
