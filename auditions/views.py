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
import json

@login_required
def prefsheet(request, show_slug):
    show = get_object_or_404(Show, slug=show_slug)
    user = request.user

    if not show.prefsheets_open:
        return render(request, 'auditions/closed.html', {'show': show})
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
        prefsheet_form = PrefSheetForm(request.POST,instance=prefsheet)

        # We reset the prefs for each post...this is ugly
        # and should be fixed ASAP
        prefsheet.prefs.all().delete()
        request.POST['prefs-INITIAL_FORMS'] = 0

        pref_formset = PrefFormSet(request.POST, instance=prefsheet)
        if user_profile_form.is_valid() and prefsheet_form.is_valid() and pref_formset.is_valid():
            profile = user_profile_form.save(commit=False)
            profile.user = user
            profile.save()
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
    return render(request, 'auditions/prefsheet.html',
                              {'show': show,
                               'user_profile_form': user_profile_form,
                               'prefsheet_form': prefsheet_form,
                               'pref_formset': pref_formset},
                              context_instance = RequestContext(request))

def thanks(request, show_slug):
    return render(request, 'auditions/thanks.html',
                              context_instance=RequestContext(request))
'''
/auditions/showslug/something
'''

def selection(request, show_slug, dance_id):
    return render(request, 'auditions/selection.html', {})
    prefs = selection_prefsheets(show_slug, dance_id)
    dance = Dance.objects.get(id=dance_id)
    dancers = [dancer.first_name+" "+dancer.last_name for dancer in dance.dancers.all()]
    return render(request, 'auditions/selection.html', {'prefs':prefs})

def selection_prefsheets(request, show_slug, dance_id):
    dance = Dance.objects.get(id=dance_id)
    all_prefs = Pref.objects.filter(dance=dance)
    prefsheets = [pref.prefsheet for pref in all_prefs]
    prefs = []
    for prefsheet in prefsheets:
        #Prefsheet model: user, conflicts, desired_dances, dances_accepted, dances_rejected
        #{key:k value for (key, value) in sequence}
        #return prefsheet.user.name, prefsheet.user.id, all the info
        user = prefsheet.user
        pref = {}
        pref['dance_id'] = dance_id
        pref['prefsheet'] = {
            'conflicts': prefsheet.conflicts,
            'desired_dances': prefsheet.desired_dances,
            #'dances': user.dances,#where show_slug = show_slug
        }
        pref['user'] = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender' : user.get_profile().get_gender_display(),
            'year': user.get_profile().year,
            'affiliation': user.get_profile().get_affiliation_display(),
            'living_group': user.get_profile().living_group,
            'experience': user.get_profile().experience,
        }
        if prefsheet.user.get_profile().photo:
            pref['user']['photo'] = prefsheet.user.get_profile().photo.url
        dances = [{'id':p.dance.id, 'name':p.dance.name, 'pref':p.pref} for p in prefsheet.prefs.all()]
        pref['dances'] = dances
        prefs.append(pref)
    return HttpResponse(json.dumps(prefs))

def accept_dancer(request, show_slug, dancer_id, dance_id):
    user = User.get(id=dancer_id)
    dance = Dance.get(id=dance_id)
    show = show.get(slug = show_slug)
    prefsheet = PrefSheet.get(user=user, show=show)
    if prefsheet.accepted_dances+prefsheet.rejected_dances>=prefsheet.desired_dances:
        return {'successful': False}
    else:
        user.dances.add(dance)
        prefsheet.accepted_dances+=1
        rtn = {}
        return {'successful': True}

def reject_dancer(request, show_slug):
    user = User.get(id=dancer_id)
    dance = Dance.get(id=dance_id)
    show = show.get(slug = show_slug)
    prefsheet = PrefSheet.get(user=user, show=show)
    prefsheet.rejected_dances+=1
    rtn = {}
    return {'successful': True, 'dances': [dancer.dances.where(show=show)],
                        'rejected': prefsheet.rejected_dances, 'accepted': prefsheet.accepted_dances}

@permission_required('auditions.can_list')
def dancesheets(request, show_slug):
    show = get_object_or_404(Show, slug=show_slug)
    dances = get_list_or_404(Dance, show=show)
    return render(request, 'auditions/dancesheets.html',
                              {'dances': dances,
                               'show': show})

@permission_required('auditions.can_list')
def prefsheets(request, show_slug):
    show = get_object_or_404(Show, slug=show_slug)
    prefsheets = PrefSheet.objects.filter(show=show).extra(
            select={'first_pref': 'SELECT dance_id FROM auditions_pref WHERE pref=1 AND prefsheet_id=auditions_prefsheet.id'},
            order_by=['first_pref'])
    return render(request, 'auditions/prefsheets.html',
                              {'prefsheets': prefsheets,
                               'show': show})

@permission_required('auditions.can_list')
def assignments(request, show_slug):
    show = get_object_or_404(Show, slug=show_slug)
    prefsheets = PrefSheet.objects.filter(show=show).order_by('user__last_name',
                                                              'user__first_name')
    return render(request, 'auditions/assignments.html',
                              {'prefsheets': prefsheets,
                               'show': show})

@permission_required('auditions.can_list')
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

@permission_required('auditions.can_list')
def emails(request, show_slug):
    show = get_object_or_404(Show, slug=show_slug)

    import csv
    response = HttpResponse(mimetype='text/csv')
    filename = '%s-auditions.csv' % show_slug
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    writer = csv.writer(response)

    prefsheets = PrefSheet.objects.filter(show=show)
    for prefsheet in prefsheets:
        writer.writerow([prefsheet.user.email])

    return response

