from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('staff/', include('staff.urls')),
    path('kitchen/', include('kitchen.urls')),
    path('tasks/', include('tasks_app.urls')),
]
