from django import forms
from django.contrib.auth.models import User
from .models import StaffProfile, LeaveRecord, AdvanceRequest


class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = '__all__'
        widgets = {'salary_date': forms.NumberInput(attrs={'min': 1, 'max': 31})}


class StaffCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label='Confirm Password')

    class Meta:
        model = StaffProfile
        fields = ['name', 'phone', 'email', 'role', 'custom_role', 'photo',
                  'is_active', 'salary_amount', 'salary_date', 'deduction_type', 'deduction_value']
        widgets = {'salary_date': forms.NumberInput(attrs={'min': 1, 'max': 31})}

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken.')
        return username

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirm = cleaned.get('confirm_password')
        if password and confirm and password != confirm:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned

    def save(self, commit=True):
        staff = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        )
        staff.user = user
        if commit:
            staff.save()
        return staff


class StaffEditForm(StaffProfileForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['display_username'] = forms.CharField(
                initial=self.instance.user.username,
                disabled=True,
                required=False,
                label='Username'
            )
            # Move to top of fields
            username_field = self.fields.pop('display_username')
            self.fields = {'display_username': username_field, **self.fields}


class LeaveForm(forms.ModelForm):
    class Meta:
        model = LeaveRecord
        fields = ['date', 'leave_type', 'note']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}


class AdvanceForm(forms.ModelForm):
    class Meta:
        model = AdvanceRequest
        fields = ['amount', 'note']
