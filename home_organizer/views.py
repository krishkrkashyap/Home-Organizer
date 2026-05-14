from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def redirect_on_login(request):
    """Redirect users to role-appropriate dashboard after login."""
    if request.user.is_superuser:
        return redirect('dashboard')
    try:
        staff = request.user.staff_profile
        return redirect('staff:my_dashboard')
    except Exception:
        return redirect('dashboard')


@login_required
def dashboard(request):
    from staff.models import StaffProfile
    from kitchen.models import PantryItem
    from tasks_app.models import AssignedTask, Reminder
    return render(request, 'dashboard.html', {
        'staff_count': StaffProfile.objects.filter(is_active=True).count(),
        'pantry_count': PantryItem.objects.count(),
        'pending_tasks': AssignedTask.objects.filter(is_completed=False).count(),
        'upcoming_reminders': Reminder.objects.filter(is_completed=False).count(),
    })
