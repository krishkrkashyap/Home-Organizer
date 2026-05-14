from django import forms
from .models import TaskTemplate, AssignedTask, Reminder

class TaskTemplateForm(forms.ModelForm):
    class Meta:
        model = TaskTemplate
        fields = '__all__'

class AssignTaskForm(forms.Form):
    staff = forms.ModelChoiceField(queryset=None, label='Staff Member')
    task_template = forms.ModelChoiceField(queryset=None, label='Task')
    assigned_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from staff.models import StaffProfile
        self.fields['staff'].queryset = StaffProfile.objects.filter(is_active=True)
        self.fields['task_template'].queryset = TaskTemplate.objects.all()

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = '__all__'
        widgets = {'due_date': forms.DateInput(attrs={'type': 'date'})}
