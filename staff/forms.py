from django import forms
from .models import StaffProfile

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = '__all__'
        widgets = {
            'salary_date': forms.NumberInput(attrs={'min': 1, 'max': 31}),
        }
