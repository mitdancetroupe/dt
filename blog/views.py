from django.shortcuts import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from dt.blog.models import *


def latest(request):
    """
    Lists posts by latest first, paginating 10 at a time.
    """
    post_list = Post.objects.exclude(hidden = True).order_by('-created')
    paginator = Paginator(post_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        posts = paginator.page(page)
    except EmptyPage, InvalidPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/latest.html', {'posts': posts},
                              context_instance = RequestContext(request))
