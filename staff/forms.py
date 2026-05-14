from django import forms
from .models import StaffProfile, LeaveRecord, AdvanceRequest

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = '__all__'
        widgets = {'salary_date': forms.NumberInput(attrs={'min': 1, 'max': 31})}

class LeaveForm(forms.ModelForm):
    class Meta:
        model = LeaveRecord
        fields = ['date', 'leave_type', 'note']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

class AdvanceForm(forms.ModelForm):
    class Meta:
        model = AdvanceRequest
        fields = ['amount', 'note']
