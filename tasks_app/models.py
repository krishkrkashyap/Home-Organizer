from django.db import models
from staff.models import StaffProfile

class TaskCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'task categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class TaskTemplate(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('one_time', 'One Time'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    day_of_week = models.IntegerField(null=True, blank=True, help_text='0=Mon to 6=Sun (for weekly)')
    day_of_month = models.IntegerField(null=True, blank=True, help_text='1-31 (for monthly)')

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        cat = f' [{self.category.name}]' if self.category else ''
        return f'{self.name} ({self.get_frequency_display()}){cat}'

class AssignedTask(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='tasks')
    task_template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-assigned_date']
        unique_together = ['staff', 'task_template', 'assigned_date']

    def __str__(self):
        status = '✅' if self.is_completed else '❌'
        return f'{status} {self.task_template.name} - {self.staff.name} ({self.assigned_date})'

class Reminder(models.Model):
    CATEGORY_CHOICES = [
        ('subscription', 'Subscription'),
        ('maintenance', 'Maintenance'),
        ('pest', 'Pest Control'),
        ('other', 'Other'),
    ]
    REPEAT_CHOICES = [
        ('none', 'No Repeat'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    repeat = models.CharField(max_length=20, choices=REPEAT_CHOICES, default='none')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title
