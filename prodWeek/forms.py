from django.forms import fields, widgets
from django.forms import ValidationError
from django.forms.models import inlineformset_factory, ModelForm
from dt.prodWeek.models import *

class PrefSheetForm(ModelForm):
    DESIRED_INTS = zip(range(1, 5), range(1, 5))
    desired_dances = fields.TypedChoiceField(choices=DESIRED_INTS, coerce=int)
    class Meta:
        model = PrefSheet
        exclude = ('user','show', 'audition_number', 'accepted_dances', 'rejected_dances',)
    class Media:
        js = ('js/vendor/jquery.js',)

class PrefForm(ModelForm):
    pref = fields.IntegerField(min_value=1,
                               widget=widgets.TextInput(attrs={'size': 2}))
    class Meta:
        model = Pref

PrefFormSet = inlineformset_factory(PrefSheet, Pref, form=PrefForm,
                                        max_num=10, extra=10)



