from django import forms
from .models import Sentinel

class UploadForm(forms.ModelForm):
    class Meta:
        model = Sentinel
        fields = ('name', 'description', 'file', 'color_ramps',)