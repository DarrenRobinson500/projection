from django import forms
from .models import *

WIDGETS = {
    'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Variable Name"}),
    'round': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Decimal Places"}),
    'formula': forms.Textarea(attrs={'class': 'form-control', 'placeholder':"Variable Formula"}),
}

class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
        fields = ['name', 'formula', 'round']
        widgets = WIDGETS