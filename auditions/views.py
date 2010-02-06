from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import *
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import inlineformset_factory, ModelForm
from django.template import RequestContext

from dt.shows.models import *
from dt.accounts.forms import *
from dt.auditions.models import *
from dt.auditions.forms import *

@login_required
def prefsheet(request, show_slug):
    show = get_object_or_404(Show, slug=show_slug)
    user = request.user

    try:
        prefsheet = PrefSheet.objects.get(user=user, show=show)
    except PrefSheet.DoesNotExist:
        prefsheet = PrefSheet(user=user, show=show)

    if request.method == 'POST':
        try:
            user_profile_form = UserProfileForm(request.POST, request.FILES,
                                                instance=user.get_profile())
        except UserProfile.DoesNotExist:
            user_profile_form = UserProfileForm(request.POST, request.FILES)
        prefsheet_form = PrefSheetForm(request.POST, instance=prefsheet)
        pref_formset = PrefFormSet(request.POST, instance=prefsheet)
        if user_profile_form.is_valid() and prefsheet_form.is_valid() and pref_formset.is_valid():
            user_profile_form.save()
            prefsheet = prefsheet_form.save()
            pref_formset.save()
            return HttpResponseRedirect('../thanks/')
    else:
        try:
            user_profile_form = UserProfileForm(instance=user.get_profile())
        except UserProfile.DoesNotExist:
            user_profile_form = UserProfileForm()
        prefsheet_form = PrefSheetForm(instance=prefsheet)
        pref_formset = PrefFormSet(instance=prefsheet)

    for pref_form in pref_formset.forms:
        pref_form.fields['dance'].queryset = Dance.objects.filter(show=show)
    return render_to_response('auditions/prefsheet.html', 
                              {'show': show,
                               'user_profile_form': user_profile_form,
                               'prefsheet_form': prefsheet_form,
                               'pref_formset': pref_formset},
                              context_instance = RequestContext(request)) 

def thanks(request, show_slug):
    return render_to_response('auditions/thanks.html', 
                              context_instance=RequestContext(request))

@permission_required('prefsheet.can_list')
def dancesheets(request, show_slug):
    show = get_object_or_404(Show, slug=show_slug)
    dances = get_list_or_404(Dance, show=show)
    return render_to_response('auditions/dancesheets.html',
                              {'dances': dances,
                               'show': show})

@permission_required('prefsheet.can_list')
def prefsheets(request, show_slug):
    show = get_object_or_404(Show, slug=show_slug)
    prefsheets = PrefSheet.objects.filter(show=show)
    return render_to_response('auditions/prefsheets.html',
                              {'prefsheets': prefsheets,
                               'show': show})

@permission_required('prefsheet.can_list')
def assignments(request, show_slug):
    show = get_object_or_404(Show, slug=show_slug)
    prefsheets = PrefSheet.objects.filter(show=show).order_by('user__last_name',
                                                              'user__first_name')
    return render_to_response('auditions/assignments.html',
                              {'prefsheets': prefsheets,
                               'show': show})

@permission_required('prefsheet.can_list')
def csv(request, show_slug):
    """
    Creates a CSV dump of dance sheets and assignments.
    """
    show = get_object_or_404(Show, slug=show_slug)
    dances = get_list_or_404(Dance, show=show)

    import csv
    response = HttpResponse(mimetype='text/csv')
    filename = '%s-auditions.csv' % show_slug
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    writer = csv.writer(response)

    for dance in dances:
        writer.writerow([dance])

        prefs = dance.prefs.order_by('prefsheet', 'pref').all()
        writer.writerow(["Dancers by Audition Number"])
        writer.writerow(["Audition Number", "Pref", "Name"])
        for pref in prefs:
            writer.writerow([pref.prefsheet.audition_number,
                             pref.pref,
                             pref.prefsheet.user.get_full_name()])
        writer.writerow([])

        prefs = dance.prefs.order_by('pref', 'prefsheet').all()
        writer.writerow(["Dancers by Pref"])
        writer.writerow(["Pref", "Audition Number", "Name"])
        for pref in prefs:
            writer.writerow([pref.pref,
                             pref.prefsheet.audition_number,
                             pref.prefsheet.user.get_full_name()])
        writer.writerow([])
        writer.writerow([])

    return response

