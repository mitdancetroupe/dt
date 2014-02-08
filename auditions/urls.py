from django.conf.urls.defaults import *

urlpatterns = patterns('dt.auditions.views',
    (r'^prefsheet/$', 'prefsheet'),
    (r'^thanks/$', 'thanks'),
    (r'^dancesheets/$', 'dancesheets'),
    (r'^prefsheets/$', 'prefsheets'),
    (r'^assignments/$', 'assignments'),
    (r'^csv/$', 'csv'),
    (r'^emails/$', 'emails'),
    (r'^selection/(?P<dance_id>\d+)$', 'selection'),
    (r'^selection_prefsheets/(?P<dance_id>\d+)$', 'selection_prefsheets'),
    (r'^accept_dancer/$', 'accept_dancer'),
    (r'^reject_dancer/(?P<dancer_id>\d+)$', 'reject_dancer'),
    (r'^selection/$', 'select_dance'),
)