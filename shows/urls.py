from django.conf.urls.defaults import *

urlpatterns = patterns('dt.shows.views',
    (r'^$', 'show_list'),
    (r'^(?P<show_slug>[\w-]+)/$', 'show_detail'),
    (r'^(?P<show_slug>[\w-]+)/print$', 'show_print'),
)