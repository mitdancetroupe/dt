from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import login, logout
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^dt/', include('dt.foo.urls')),

    # Development version serving of static files
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                              {'document_root': settings.MEDIA_ROOT}),

    # Admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    # Accounts
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/profile/$', 'dt.core.views.profile'),

    (r'^auditions/prefsheet/$', 'dt.auditions.views.prefsheet'),
)
