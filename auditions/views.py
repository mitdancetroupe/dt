from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory, ModelForm
from django.template import RequestContext

from dt.core.models import Show
from dt.core.forms import *
from dt.auditions.models import *
from dt.auditions.forms import *

@login_required
def prefsheet(request, semester, year):
    semester = {'S': 0, 'F': 1}[semester]
    year = 2000 + int(year) # This is a really ugly hack, but whatever
    show = Show.objects.get(year=year, semester=semester)
    user = request.user
    
    try:
        prefsheet = PrefSheet.objects.get(user=user, show=show)
    except PrefSheet.DoesNotExist:
        prefsheet = PrefSheet(user=user, show=show)

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, 
                                            instance=user.get_profile())
        prefsheet_form = PrefSheetForm(request.POST, instance=prefsheet)
        pref_formset = PrefFormSet(request.POST, instance=prefsheet)
        if user_profile_form.is_valid() and prefsheet_form.is_valid() and pref_formset.is_valid():
            user_profile_form.save()
            prefsheet_form.save()
            pref_formset.save()
            return HttpResponseRedirect(reverse('dt.auditions.views.thanks'))
    else:
        user_profile_form = UserProfileForm(instance=user.get_profile())
        prefsheet_form = PrefSheetForm(instance=prefsheet)
        pref_formset = PrefFormSet(instance=prefsheet)

    return render_to_response('auditions/prefsheet.html', 
                              {'show': show,
                               'user_profile_form': user_profile_form,
                               'prefsheet_form': prefsheet_form,
                               'pref_formset': pref_formset},
                              context_instance = RequestContext(request)) 

