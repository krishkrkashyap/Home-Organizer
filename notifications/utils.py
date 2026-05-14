from datetime import timedelta, date
from django.utils import timezone
from .models import Notification


def generate_alerts(user):
    """On-demand checks: create notifications for time-sensitive alerts."""
    today = timezone.now().date()

    if user.is_superuser:
        _check_overdue_tasks_admin(user, today)
        _check_salary_reminders(user, today)
        _check_reminders(user, today)
    else:
        _check_overdue_tasks_staff(user, today)


def _already_notified_today(user, ntype):
    return Notification.objects.filter(
        recipient=user, type=ntype,
        created_at__date=timezone.now().date()
    ).exists()


def _check_overdue_tasks_admin(user, today):
    """Notify admin of all overdue tasks across staff."""
    from tasks_app.models import AssignedTask
    overdue = AssignedTask.objects.filter(
        is_completed=False, assigned_date__lt=today
    )
    if overdue.exists() and not _already_notified_today(user, 'task_overdue'):
        count = overdue.count()
        Notification.objects.create(
            recipient=user,
            title='Overdue Tasks',
            message=f'{count} task(s) are overdue. Check task dashboard.',
            type='task_overdue',
            link='/tasks/',
        )


def _check_overdue_tasks_staff(user, today):
    """Notify staff of their own overdue tasks."""
    try:
        staff = user.staff_profile
    except Exception:
        return
    from tasks_app.models import AssignedTask
    overdue = AssignedTask.objects.filter(
        staff=staff, is_completed=False, assigned_date__lt=today
    )
    if overdue.exists() and not _already_notified_today(user, 'task_overdue'):
        count = overdue.count()
        Notification.objects.create(
            recipient=user,
            title='Your Overdue Tasks',
            message=f'You have {count} overdue task(s).',
            type='task_overdue',
            link='/staff/my/tasks/',
        )


def _check_salary_reminders(user, today):
    """Notify admin of upcoming salary dates (within 3 days)."""
    from staff.models import StaffProfile
    upcoming = StaffProfile.objects.filter(is_active=True)
    for staff in upcoming:
        due = _next_salary_date(staff.salary_date, today)
        if due and 0 <= (due - today).days <= 3:
            key = f'salary_{staff.id}'
            if not _already_notified_today(user, key):
                Notification.objects.create(
                    recipient=user,
                    title='Salary Due',
                    message=f'{staff.name} salary of ₹{staff.salary_amount} due on {due}',
                    type='salary_reminder',
                    link=f'/staff/{staff.pk}/salary/',
                )


def _check_reminders(user, today):
    """Notify admin of reminders due within 3 days."""
    from tasks_app.models import Reminder
    upcoming = Reminder.objects.filter(
        is_completed=False, due_date__gte=today,
        due_date__lte=today + timedelta(days=3)
    )
    for r in upcoming:
        key = f'reminder_{r.id}'
        if not _already_notified_today(user, key):
            Notification.objects.create(
                recipient=user,
                title='Reminder Coming Up',
                message=f'"{r.title}" is due on {r.due_date}',
                type='reminder_due',
                link='/tasks/reminders/',
            )


def _next_salary_date(day, today):
    """Calculate the next salary date from today."""
    if day < 1 or day > 31:
        return None
    year, month = today.year, today.month
    try:
        candidate = date(year, month, day)
    except ValueError:
        import calendar
        last = calendar.monthrange(year, month)[1]
        candidate = date(year, month, min(day, last))
    if candidate < today:
        month += 1
        if month > 12:
            month = 1
            year += 1
        try:
            candidate = date(year, month, day)
        except ValueError:
            last = calendar.monthrange(year, month)[1]
            candidate = date(year, month, min(day, last))
    return candidate
