from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
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
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                title='New Reminder',
                message=f'Reminder: {instance.title} due on {instance.due_date}',
                type='reminder_due',
                link='/tasks/reminders/',
            )


@receiver(post_save, sender='staff.LeaveRecord')
def notify_admin_leave(sender, instance, created, **kwargs):
    """Notify admin when staff applies for leave."""
    if created:
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                title='Leave Applied',
                message=f'{instance.staff.name} applied {instance.get_leave_type_display()} on {instance.date}',
                type='reminder_due',
                link=f'/staff/{instance.staff.pk}/',
            )


@receiver(post_save, sender='staff.AdvanceRequest')
def notify_admin_advance(sender, instance, created, **kwargs):
    """Notify admin when staff requests an advance."""
    if created:
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                title='Advance Requested',
                message=f'{instance.staff.name} requested ₹{instance.amount} advance',
                type='salary_reminder',
                link=f'/staff/{instance.staff.pk}/',
            )
