from django.conf.urls.defaults import *

urlpatterns = patterns('dt.auditions.views',
    (r'^prefsheet/$', 'prefsheet'),
    (r'^thanks/$', 'thanks'),
    (r'^dancesheets/$', 'dancesheets'),
    (r'^prefsheets/$', 'prefsheets'),
    (r'^assignments/$', 'assignments'),
    (r'^csv/$', 'csv'),
)
