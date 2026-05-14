from django import forms
from .models import TaskTemplate, AssignedTask, Reminder

class TaskTemplateForm(forms.ModelForm):
    class Meta:
        model = TaskTemplate
        fields = '__all__'

class AssignTaskForm(forms.Form):
    staff = forms.ModelChoiceField(queryset=None, label='Staff Member')
    task_template = forms.ModelChoiceField(queryset=None, label='Task')
    assigned_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes for this assignment...'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from staff.models import StaffProfile
        self.fields['staff'].queryset = StaffProfile.objects.filter(is_active=True)
        self.fields['task_template'].queryset = TaskTemplate.objects.select_related('category').all()
        self.fields['task_template'].label_from_instance = lambda obj: f'{obj.name} ({obj.get_frequency_display()})'

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = '__all__'
        widgets = {'due_date': forms.DateInput(attrs={'type': 'date'})}
