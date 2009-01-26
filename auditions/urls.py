from django.conf.urls.defaults import *

urlpatterns = patterns('dt.auditions.views',
    (r'^prefsheet/$', 'prefsheet'),
    (r'^thanks/$', 'thanks'),
    (r'^dances/$', 'dances'),
    (r'^dancesheets/$', 'dancesheets'),
    (r'^prefsheets/$', 'prefsheets'),
    (r'^assignments/$', 'assignments'),
)
