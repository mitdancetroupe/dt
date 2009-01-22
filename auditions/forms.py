from django.forms import fields, widgets
from django.forms import ValidationError
from django.forms.models import inlineformset_factory, ModelForm
from dt.auditions.models import *

class PrefSheetForm(ModelForm):
    DESIRED_INTS = zip(range(1, 5), range(1, 5))
    desired_dances = fields.TypedChoiceField(choices=DESIRED_INTS, coerce=int)
    class Meta:
        model = PrefSheet
        exclude = ('user','show', 'audition_number',)
    class Media:
        js = ('js/jquery.js',)
 
class PrefForm(ModelForm):
    pref = fields.IntegerField(min_value=1, 
                               widget=widgets.TextInput(attrs={'size': 2}))
    class Meta:
        model = Pref

BasePrefFormSet = inlineformset_factory(PrefSheet, Pref, form=PrefForm, 
                                        max_num=10, extra=10)

class PrefFormSet(BasePrefFormSet):
    
    def clean(self):
        self.validate_unique()
    
    def validate_unique(self):
        from django.db.models.fields import FieldDoesNotExist
        unique_checks = []
        for name, field in self.forms[0].fields.iteritems():
            try:
                f = self.forms[0].instance._meta.get_field_by_name(name)[0]
            except FieldDoesNotExist:
                continue
            if f.unique:
                unique_checks.append((name,))
        unique_together = self.forms[0].instance._meta.unique_together
        unique_together = [check for check in unique_together if [True for field in check if field in self.forms[0].fields]]
        unique_checks.extend(unique_together)

        errors = []
        for unique_check in unique_checks:
            data = set()
            for i in xrange(self._total_form_count):
                form = self.forms[i]
                if not hasattr(form, 'cleaned_data'):
                    continue
                if [True for field in unique_check if field in form.cleaned_data and form.cleaned_data[field] is not None]:
                    instance = tuple([form.cleaned_data[field] for field in unique_check])
                    if instance in data:
                        if len(unique_check) == 1:
                            errors.append(_("You have entered duplicate data for %(field)s, all %(field)ss should be unique.") % {
                                    'field': unique_check[0],
                                })
                        else:
                            errors.append(_("You have entered duplicate data for %(field)s, %(field)s should be unique together.") % {
                                    'field': get_text_list(unique_check, _("and")),
                                })
                        break
                    else:
                        data.add(instance)

        if errors:
            raise ValidationError(errors)



