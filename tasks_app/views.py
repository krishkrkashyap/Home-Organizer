import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import TaskTemplate, AssignedTask, Reminder, TaskCategory
from .forms import TaskTemplateForm, AssignTaskForm, ReminderForm


@login_required
def task_dashboard(request):
    today = timezone.now().date()
    today_tasks = AssignedTask.objects.filter(assigned_date=today).select_related('staff', 'task_template', 'task_template__category')
    pending_tasks = AssignedTask.objects.filter(is_completed=False).select_related('staff', 'task_template')[:20]
    return render(request, 'tasks_app/task_dashboard.html', {
        'today': today,
        'today_tasks': today_tasks,
        'pending_tasks': pending_tasks,
    })


@login_required
def task_list(request):
    tasks = AssignedTask.objects.all().select_related('staff', 'task_template').order_by('-assigned_date')
    return render(request, 'tasks_app/task_list.html', {'tasks': tasks})


@login_required
def task_assign(request):
    # Build JSON for task details preview
    templates = TaskTemplate.objects.select_related('category').all()
    task_data = {}
    for t in templates:
        task_data[t.pk] = {
            'name': t.name,
            'description': t.description or 'No description provided.',
            'category': t.category.name if t.category else '—',
            'frequency': t.get_frequency_display(),
        }

    if request.method == 'POST':
        form = AssignTaskForm(request.POST)
        if form.is_valid():
            staff = form.cleaned_data['staff']
            template = form.cleaned_data['task_template']
            date = form.cleaned_data['assigned_date']
            notes = form.cleaned_data.get('notes', '')
            AssignedTask.objects.get_or_create(
                staff=staff, task_template=template, assigned_date=date,
                defaults={'is_completed': False, 'notes': notes}
            )
            messages.success(request, f'Task assigned to {staff.name}.')
            return redirect('tasks_app:task_dashboard')
    else:
        form = AssignTaskForm()
    return render(request, 'tasks_app/task_assign.html', {
        'form': form,
        'task_data_json': json.dumps(task_data),
    })


@login_required
def task_toggle(request, pk):
    task = get_object_or_404(AssignedTask, pk=pk)
    task.is_completed = not task.is_completed
    task.completed_at = timezone.now() if task.is_completed else None
    task.save()
    messages.success(request, f'Task {"completed" if task.is_completed else "reopened"}.')
    return redirect(request.META.get('HTTP_REFERER', 'tasks_app:task_dashboard'))


@login_required
def task_delete(request, pk):
    task = get_object_or_404(AssignedTask, pk=pk)
    task.delete()
    messages.success(request, 'Task deleted.')
    return redirect('tasks_app:task_dashboard')

# --- Reminders ---

@login_required
def reminder_list(request):
    reminders = Reminder.objects.all().order_by('due_date')
    return render(request, 'tasks_app/reminder_list.html', {'reminders': reminders, 'today': timezone.now().date()})


@login_required
def reminder_create(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reminder created.')
            return redirect('tasks_app:reminder_list')
    else:
        form = ReminderForm()
    return render(request, 'tasks_app/reminder_form.html', {'form': form, 'title': 'Add Reminder'})


@login_required
def reminder_edit(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk)
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reminder updated.')
            return redirect('tasks_app:reminder_list')
    else:
        form = ReminderForm(instance=reminder)
    return render(request, 'tasks_app/reminder_form.html', {'form': form, 'title': 'Edit Reminder'})


@login_required
def reminder_toggle(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk)
    reminder.is_completed = not reminder.is_completed
    reminder.save()
    return redirect('tasks_app:reminder_list')


@login_required
def reminder_delete(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk)
    reminder.delete()
    messages.success(request, 'Reminder deleted.')
    return redirect('tasks_app:reminder_list')
