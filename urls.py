from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    # Example:
    # (r'^dt/', include('dt.foo.urls')),

    # Development version serving of static files
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                              {'document_root': settings.MEDIA_ROOT}),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^auditions/prefsheet/$', 'dt.auditions.views.prefsheet'),
)
