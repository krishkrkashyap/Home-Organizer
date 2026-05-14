from django.contrib import admin
from .models import TaskCategory, TaskTemplate, AssignedTask, Reminder

@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(TaskTemplate)
class TaskTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'frequency']
    list_filter = ['frequency']

@admin.register(AssignedTask)
class AssignedTaskAdmin(admin.ModelAdmin):
    list_display = ['staff', 'task_template', 'assigned_date', 'is_completed']
    list_filter = ['is_completed', 'assigned_date']

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'category', 'is_completed']
    list_filter = ['category', 'is_completed']
