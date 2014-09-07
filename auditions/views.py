import json

from django.views.decorators.csrf import csrf_exempt
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

def get_dancers(dance, show_slug):
    dancers = []
    show = Show.objects.get(slug=show_slug)
    for dancer in dance.dancers.all():
        prefsheet = PrefSheet.objects.get(user=dancer, show=show)
        pref = Pref.objects.get(prefsheet=prefsheet, dance=dance)
        dancers.append({'id': dancer.id, 'name': dancer.first_name+" "+dancer.last_name, 'conflicts':prefsheet.conflicts, 'email': dancer.email})
    return dancers

@permission_required('auditions.can_list')
def select_dance(request, show_slug):
    show = Show.objects.get(slug=show_slug)
    dances = Dance.objects.filter(show=show)
    return render(request, 'auditions/dance_selection.html', {'dances':dances, 'show_slug':show_slug})

@permission_required('auditions.can_list')
def selection(request, show_slug, dance_id):
    return render(request, 'auditions/selection.html', {'slug':show_slug, 'dance_id':dance_id})

def dancers(request, show_slug, dance_id):
    dance = Dance.objects.get(id=dance_id)
    context = {}
    dancers = get_dancers(dance, show_slug)
    context['dancers'] = dancers
    return HttpResponse(json.dumps(context), content_type="application/json")


def future_prefs(request, show_slug, dance_id):
    dance = Dance.objects.get(id=dance_id)
    #initialize context
    context = {}
    context['dancers'] = []
    #get the prefs
    all_prefs = Pref.objects.filter(dance=dance).order_by('pref')
    for pref in all_prefs:
        prefsheet = pref.prefsheet
        desired_dances = prefsheet.desired_dances
        rejected_dances = prefsheet.prefs.filter(accepted=False).count()
        accepted_dances = prefsheet.prefs.filter(accepted=True).count()
        prefed = prefsheet.prefs.count()
        if accepted_dances >= prefsheet.desired_dances:
            continue
        if pref.accepted:
            continue
        if pref.accepted is False and not pref.return_if_not_placed:
            continue

        return_window = window = Pref.objects.filter(prefsheet=prefsheet, return_if_not_placed=True).order_by('pref')[:1]
        if pref in return_window and rejected_dances >= prefed:
            continue

        #Sliding Window logic
        window_size = desired_dances-accepted_dances
        window = Pref.objects.filter(prefsheet=prefsheet, accepted=None).order_by('pref')[:window_size]
        if pref in window:
            continue
        dances_looking_at_pref = ', '.join([p.dance.name for p in window])
        user = prefsheet.user
        pref_dict = {
            'desired': desired_dances,
            'prefed': prefed,
            'audition': pref.prefsheet.audition_number,
            'pref': pref.pref,
            'name': user.first_name + " " + user.last_name,
            'accepted': accepted_dances,
            'rejected': rejected_dances,
            'window': dances_looking_at_pref,
            'not_placed': pref.return_if_not_placed
        }
        context['dancers'].append(pref_dict)
    return HttpResponse(json.dumps(context), content_type="application/json")


def prefs(request, show_slug, dance_id):
    dance = Dance.objects.get(id=dance_id)
    #initialize context
    context = {}
    context['dancers'] = []
    #get the prefs
    all_prefs = Pref.objects.filter(dance=dance)
    for pref in all_prefs:
        prefsheet = pref.prefsheet
        desired_dances = prefsheet.desired_dances
        rejected_dances = prefsheet.prefs.filter(accepted=False).count()
        accepted_dances = prefsheet.prefs.filter(accepted=True).count()
        if pref.return_if_not_placed and rejected_dances == prefsheet.prefs.count():
            window = Pref.objects.filter(prefsheet=prefsheet, return_if_not_placed=True).order_by('pref')[:1]
            if pref not in window:
                continue
            pref.accepted = None
            pref.save()
        if pref.accepted is not None or accepted_dances >= prefsheet.desired_dances:
            continue
        #Sliding Window logic
        window_size = desired_dances-accepted_dances
        window = Pref.objects.filter(prefsheet=prefsheet, accepted=None).order_by('pref')[:window_size]
        if pref not in window:
            continue
        # end sliding window logic
        user = prefsheet.user
        pref_dict = {
            'dance_id': dance_id,
            'slug': show_slug,
            'conflicts': prefsheet.conflicts,
            'desired': desired_dances,
            'prefed': prefsheet.prefs.count(),
            'audition': pref.prefsheet.audition_number,
            'pref': pref.pref,
            'dancer_id': user.id,
            'pref_id': pref.id,
            'name': user.first_name + " " + user.last_name,
            'gender': user.get_profile().get_gender_display(),
            'year': user.get_profile().year,
            'affiliation': user.get_profile().get_affiliation_display(),
            'living_group': user.get_profile().living_group,
            'experience': user.get_profile().experience,
            'accepted': accepted_dances,
            'rejected': rejected_dances,
            'not_placed': pref.return_if_not_placed
        }
        dances = [{'id': p.dance.id, 'name': p.dance.name, 'pref': p.pref, 'accepted': p.accepted} for p in prefsheet.prefs.all()]
        pref_dict['dances'] = dances
        if prefsheet.user.get_profile().photo:
            pref_dict['photo'] = prefsheet.user.get_profile().photo.url
        context['dancers'].append(pref_dict)
    return HttpResponse(json.dumps(context), content_type="application/json")


def accept_dancer(request, show_slug):
    #get user
    data = json.loads(request.body)
    dancer_id = data.get("dancer_id")
    user = User.objects.get(id=dancer_id)

    #get dance
    dance_id = data.get("dance_id")
    dance = Dance.objects.get(id=dance_id)

    #get show
    show = Show.objects.get(slug=show_slug)

    #get prefsheet and pref
    prefsheet = PrefSheet.objects.get(user=user, show=show)
    pref = Pref.objects.get(dance=dance, prefsheet=prefsheet)

    accepted_dances = prefsheet.prefs.filter(accepted=True).count()

    if accepted_dances >= prefsheet.desired_dances:
        rtn = {'successful': False, 'message': 'Dancer has already been accepted into too many dances.'}
    elif pref.accepted is not None:
        rtn = {'successful': False, 'message': 'You have already made a decision on this dancer.'}
    else:
        pref.accepted = True
        pref.save()
        user.danced_in.add(dance)
        rtn = {'successful': True}
    return HttpResponse(json.dumps(rtn), content_type="application/json")


def return_dancer(request, show_slug):
    data = json.loads(request.body)
    dancer_id = data.get("dancer_id")
    dance_id = data.get("dance_id")
    user = User.objects.get(id=dancer_id)
    dance = Dance.objects.get(id=dance_id)
    show = Show.objects.get(slug=show_slug)
    prefsheet = PrefSheet.objects.get(user=user, show=show)
    pref = Pref.objects.get(dance=dance, prefsheet=prefsheet)

    accepted_dances = prefsheet.prefs.filter(accepted=True).count()

    if (accepted_dances == 0):
        pref.return_if_not_placed = True

    pref.accepted = False
    pref.save()

    rtn = {'successful': True}
    return HttpResponse(json.dumps(rtn), content_type="application/json")


def reject_dancer(request, show_slug):
    data = json.loads(request.body)
    dancer_id = data.get("dancer_id")
    dance_id = data.get("dance_id")
    user = User.objects.get(id=dancer_id)
    dance = Dance.objects.get(id=dance_id)
    show = Show.objects.get(slug=show_slug)
    prefsheet = PrefSheet.objects.get(user=user, show=show)
    pref = Pref.objects.get(dance=dance, prefsheet=prefsheet)

    pref.accepted = False
    pref.save()
    rtn = {'successful': True}
    return HttpResponse(json.dumps(rtn), content_type="application/json")

def finish_picking(request, show_slug):
    data = json.loads(request.body)
    dance_id = data.get("dance_id")
    dance = Dance.objects.get(id=dance_id)
    all_prefs = Pref.objects.filter(dance=dance)
    for pref in all_prefs:
        if not pref.accepted:
            pref.accepted = False;
            pref.return_if_not_placed = False;
            pref.save()
    return HttpResponse({'successful': 'true'}, content_type="application/json")


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

