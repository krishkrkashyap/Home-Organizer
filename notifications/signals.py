from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Notification


@receiver(post_save, sender='tasks_app.AssignedTask')
def notify_task_assigned(sender, instance, created, **kwargs):
    """Notify staff when a task is assigned."""
    if created and instance.staff and instance.staff.user:
        Notification.objects.create(
            recipient=instance.staff.user,
            title='Task Assigned',
            message=f'Task "{instance.task_template.name}" assigned for {instance.assigned_date}',
            type='task_assigned',
            link=f'/tasks/{instance.pk}/toggle/',
        )


@receiver(post_save, sender='tasks_app.Reminder')
def notify_reminder_due(sender, instance, created, **kwargs):
    """Notify admin about new reminders."""
    if created:
        from django.contrib.auth.models import User
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                title='New Reminder',
                message=f'Reminder: {instance.title} due on {instance.due_date}',
                type='reminder_due',
                link='/tasks/reminders/',
            )
