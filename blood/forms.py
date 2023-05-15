from django import forms
from . import models
from django.contrib.auth.forms import AuthenticationForm


class BloodForm(forms.ModelForm):
    class Meta:
        model=models.Stock
        fields=['bloodgroup','unit']

class RequestForm(forms.ModelForm):
    class Meta:
        model=models.BloodRequest
        fields=['patient_name','patient_age','reason','bloodgroup','unit','requisition_form']



from .models import Email

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('email', 'message')
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }



            

