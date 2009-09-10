from django.conf.urls.defaults import *
from dt.costumes.models import Costume

info_dict = {
    'queryset': Costume.objects.all()
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
)
