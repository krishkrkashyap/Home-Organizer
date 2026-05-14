from django import forms
from .models import TaskTemplate, AssignedTask, Reminder

class TaskTemplateForm(forms.ModelForm):
    class Meta:
        model = TaskTemplate
        fields = '__all__'

class AssignTaskForm(forms.Form):
    staff = forms.ModelChoiceField(queryset=None, label='Staff Member')
    task_name = forms.CharField(max_length=200, label='Task Name')
    frequency = forms.ChoiceField(choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'), 
        ('monthly', 'Monthly'),
        ('one_time', 'One Time')
    ], initial='daily', label='Frequency')
    day_of_week = forms.IntegerField(min_value=0, max_value=6, required=False, label='Day of Week (0=Mon)')
    day_of_month = forms.IntegerField(min_value=1, max_value=31, required=False, label='Day of Month (1-31)')
    assigned_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes for this assignment...'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from staff.models import StaffProfile
        self.fields['staff'].queryset = StaffProfile.objects.filter(is_active=True)

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = '__all__'
        widgets = {'due_date': forms.DateInput(attrs={'type': 'date'})}
