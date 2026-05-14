from datetime import date

from django.contrib import admin
from django.utils.html import format_html
from .models import AssignedTask, Reminder, TaskCategory, TaskTemplate


@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'task_count']
    search_fields = ['name']

    @admin.display(description='Templates')
    def task_count(self, obj):
        return obj.tasktemplate_set.count()


@admin.register(TaskTemplate)
class TaskTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'frequency', 'schedule_display', 'description_preview']
    list_filter = ['frequency', 'category']
    search_fields = ['name', 'description']
    list_select_related = ['category']
    fieldsets = [
        ('Basic Info', {'fields': ['name', 'description', 'category']}),
        ('Schedule', {'fields': ['frequency', 'day_of_week', 'day_of_month']}),
    ]

    @admin.display(description='Schedule')
    def schedule_display(self, obj):
        if obj.frequency == 'weekly' and obj.day_of_week is not None:
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            return days[obj.day_of_week]
        if obj.frequency == 'monthly' and obj.day_of_month is not None:
            return f'Day {obj.day_of_month}'
        return '—'

    @admin.display(description='Description')
    def description_preview(self, obj):
        if not obj.description:
            return '—'
        return obj.description[:80] + '...' if len(obj.description) > 80 else obj.description


@admin.register(AssignedTask)
class AssignedTaskAdmin(admin.ModelAdmin):
    list_display = ['staff', 'task_template', 'assigned_date', 'status_badge', 'completed_at', 'notes_preview']
    list_filter = ['is_completed', 'assigned_date', 'staff', 'task_template']
    search_fields = ['staff__name', 'task_template__name', 'notes']
    list_select_related = ['staff', 'task_template__category']
    date_hierarchy = 'assigned_date'
    fieldsets = [
        ('Assignment', {'fields': ['staff', 'task_template', 'assigned_date']}),
        ('Status', {'fields': ['is_completed', 'completed_at', 'notes']}),
    ]
    actions = ['mark_completed', 'mark_pending']

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.is_completed:
            return format_html('<span style="color:green;font-weight:bold;">&#10003; Completed</span>')
        return format_html('<span style="color:red;font-weight:bold;">&#10007; Pending</span>')

    @admin.display(description='Notes')
    def notes_preview(self, obj):
        if not obj.notes:
            return '—'
        return obj.notes[:60] + '...' if len(obj.notes) > 60 else obj.notes

    @admin.action(description='Mark selected as completed')
    def mark_completed(self, request, queryset):
        updated = queryset.update(is_completed=True)
        self.message_user(request, f'{updated} task(s) marked as completed.')

    @admin.action(description='Mark selected as pending')
    def mark_pending(self, request, queryset):
        updated = queryset.update(is_completed=False)
        self.message_user(request, f'{updated} task(s) marked as pending.')


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'due_date', 'overdue_badge', 'repeat', 'is_completed']
    list_filter = ['category', 'repeat', 'is_completed']
    search_fields = ['title', 'description']
    date_hierarchy = 'due_date'
    fieldsets = [
        ('Reminder Info', {'fields': ['title', 'description', 'category']}),
        ('Schedule', {'fields': ['due_date', 'repeat']}),
        ('Status', {'fields': ['is_completed']}),
    ]
    actions = ['mark_completed']

    @admin.display(description='Overdue')
    def overdue_badge(self, obj):
        if not obj.is_completed and obj.due_date < date.today():
            return format_html('<span style="color:red;font-weight:bold;">&#9888; Overdue</span>')
        elif obj.is_completed:
            return format_html('<span style="color:green;">&#10003; Done</span>')
        return '—'

    @admin.action(description='Mark selected as completed')
    def mark_completed(self, request, queryset):
        updated = queryset.update(is_completed=True)
        self.message_user(request, f'{updated} reminder(s) marked as completed.')
