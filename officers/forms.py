from django import forms

from officers.models import Officer
from tinymce.widgets import TinyMCE

class OfficerForm(forms.ModelForm):
    class Meta:
        model = Officer
