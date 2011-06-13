from django import forms

from blog.models import Post
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Post
