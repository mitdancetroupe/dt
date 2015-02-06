from django.shortcuts import *
from django.template import RequestContext
from dt.officers.models import *

def officers(request):
    officers_list = Officer.objects.order_by('order')
    return render(request, 'officers/officers.html', {'officers': officers_list},
                              context_instance=RequestContext(request))