from django.http import Http404
from django.shortcuts import *

from dt.shows.models import *

def list(request):
    shows = Show.objects.all().order_by()
    return render_to_response('shows/list.html', locals())

def detail(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    return render_to_response('shows/detail.html', locals())
