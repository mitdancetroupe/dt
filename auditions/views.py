from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from dt.core.models import Show
from dt.auditions.models import PrefSheet
from dt.auditions.forms import PrefSheetForm

@login_required
def prefsheet(request):
    show = Show.objects.all().order_by('year', 'semester')[0]
    prefs, is_new = PrefSheet.objects.get_or_create(user=request.user,show=show)
    form = PrefSheetForm()
    return render_to_response('auditions/prefsheet.html', 
                              {'form': form}) 

