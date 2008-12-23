from django.shortcuts import render_to_response

from dt.shows.models import *

def shows(request):
    shows = Show.objects().all().order_by()
    

