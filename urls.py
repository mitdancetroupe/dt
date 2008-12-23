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
    (r'^accounts/register/$', 'dt.core.views.register'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/profile/$', 'dt.core.views.profile'),

    # Shows
    (r'^shows/$', 'dt.core.views.shows'),

    (r'^auditions/(\D{1})(\d{2})/prefsheet/$', 'dt.auditions.views.prefsheet'),
    (r'^auditions/(\D{1})(\d{2})/thanks/$', 'dt.auditions.views.thanks'),
    (r'^auditions/(\D{1})(\d{2})/dances/$', 'dt.auditions.views.dances'),
    (r'^auditions/(\D{1})(\d{2})/dancesheets/$', 'dt.auditions.views.dancesheets'),
    (r'^auditions/(\D{1})(\d{2})/prefsheets/$', 'dt.auditions.views.prefsheets'),
    (r'^auditions/(\D{1})(\d{2})/assignments/$', 'dt.auditions.views.assignments'),
)
