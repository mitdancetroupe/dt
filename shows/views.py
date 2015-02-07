from django.http import Http404
from django.shortcuts import *
from django.template import RequestContext

from dt.shows.models import *

def show_list(request):
    shows = Show.objects.all().order_by('-year', 'semester')
    return render(request, 'shows/show_list.html', locals(),
                              context_instance=RequestContext(request))

def show_detail(request, show_slug):
    show = get_object_or_404(Show, slug=show_slug)
    return render(request, 'shows/show_detail.html', locals(),
                              context_instance=RequestContext(request))

def show_print(request, show_slug):
    show = get_object_or_404(Show, slug=show_slug)
    return render(request, 'shows/print.html', locals(),
                              context_instance=RequestContext(request))
