
from django import forms
from .models import Link

class AddForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('url', )