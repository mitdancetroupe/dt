from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import login, logout
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'dt.blog.views.latest'),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    (r'^accounts/', include('dt.accounts.urls')),
    (r'^shows/', include('dt.shows.urls')),
    (r'^auditions/(?P<show_slug>[\w-]+)/', include('dt.auditions.urls')),

    # Development version serving of static files
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                              {'document_root': settings.MEDIA_ROOT}),
)
