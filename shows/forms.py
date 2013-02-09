from django import forms

from shows.models import Show
from tinymce.widgets import TinyMCE

class ShowForm(forms.ModelForm):
    info = forms.CharField(widget = TinyMCE(attrs = {'cols': 80, 'rows': 30}))
    class Meta:
        model = Show
