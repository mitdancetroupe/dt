from django.http import Http404
from django.shortcuts import *

from dt.shows.models import *

def show_list(request):
    shows = Show.objects.all().order_by()
    return render_to_response('shows/show_list.html', locals())

def show_detail(request, show_slug):
    show = get_object_or_404(Show, slug=show_slug)
    return render_to_response('shows/show_detail.html', locals())
