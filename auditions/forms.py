from django.forms import fields, widgets
from django.forms import ValidationError
from django.forms.models import inlineformset_factory, ModelForm
from dt.auditions.models import *
from dt.core.models import *

class PrefSheetForm(ModelForm):
    DESIRED_INTS = zip(range(1, 5), range(1, 5))
    desired_dances = fields.TypedChoiceField(choices=DESIRED_INTS, coerce=int)
    class Meta:
        model = PrefSheet
        exclude = ('user','show', 'audition_number',)
    class Media:
        js = ('js/jquery.js', 'js/prefsheet.js',)
 
class PrefForm(ModelForm):
    pref = fields.IntegerField(min_value=1, 
                               widget=widgets.TextInput(attrs={'size': 2}))
    class Meta:
        model = Pref

PrefFormSet = inlineformset_factory(PrefSheet, Pref, form=PrefForm, 
                                    extra=10, max_num=10)


