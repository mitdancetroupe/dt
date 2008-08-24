from django.forms.models import inlineformset_factory, ModelForm
from dt.auditions.models import *

class PrefSheetForm(ModelForm):
    class Meta:
        model = PrefSheet
        exclude = ('user','show')
PrefFormSet = inlineformset_factory(PrefSheet, Pref)

