from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.contrib import databrowse

admin.autodiscover()

# from dt.costumes.models import *
# databrowse.site.register(Costume)

urlpatterns = patterns('',
    # (r'^$', 'dt.blog.views.index'),
    (r'^$', 'dt.blog.views.latest'),
    (r'^home/', 'dt.blog.views.index'),
    (r'^announcements/', 'dt.blog.views.latest'),
    (r'^officers/', 'dt.officers.views.officers'),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^accounts/', include('dt.accounts.urls')),
    (r'^shows/', include('dt.shows.urls')),
    (r'^costumes/', include('dt.costumes.urls')),
    (r'^auditions/(?P<show_slug>[\w-]+)/', include('dt.auditions.urls')),

    (r'^databrowse/(.*)', databrowse.site.root),

    # Development version serving of static files
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                              {'document_root': settings.MEDIA_ROOT}),

    (r'^tinymce/', include('tinymce.urls')),
)
