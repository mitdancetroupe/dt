from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from honeypot.decorators import check_honeypot

from dt.accounts.models import *
from dt.accounts.forms import *

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        try:
            user_profile_form = UserProfileForm(request.POST, request.FILES,
                                                instance=user.get_profile())
        except UserProfile.DoesNotExist:
            user_profile_form = UserProfileForm(request.POST, request.FILES)
        if user_profile_form.is_valid(): 
            profile = user_profile_form.save(commit=False)
            profile.user = user
            profile.save()
    else:
        try:
            user_profile_form = UserProfileForm(instance=user.get_profile())
        except UserProfile.DoesNotExist:
            user_profile_form = UserProfileForm()
    return render(request, 'accounts/profile.html', 
                              {'user_profile_form': user_profile_form})

@check_honeypot
def register(request):
    # redirect_to code taken from django.contrib.auth.views
    redirect_to = request.REQUEST.get('next', '')
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and user_profile_form.is_valid():
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            user = user_form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            return HttpResponseRedirect(redirect_to)
    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()

    return render(request, 'accounts/register.html',
                             {'user_form': user_form,
                              'user_profile_form': user_profile_form,
                               'next': redirect_to})


