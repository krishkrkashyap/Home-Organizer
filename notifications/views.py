from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages

from .models import Notification
from .utils import generate_alerts


@login_required
def notification_list(request):
    """Full notification page — generates alerts on load."""
    generate_alerts(request.user)
    notifications = Notification.objects.filter(recipient=request.user)
    type_filter = request.GET.get('type', '')
    if type_filter:
        notifications = notifications.filter(type=type_filter)
    return render(request, 'notifications/list.html', {
        'notifications': notifications,
        'current_type': type_filter,
    })


@login_required
def notification_mark_read(request, pk):
    """Toggle single notification as read. Returns JSON."""
    n = get_object_or_404(Notification, pk=pk, recipient=request.user)
    n.is_read = True
    n.save(update_fields=['is_read'])
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    messages.success(request, 'Notification marked as read.')
    return redirect('notifications:list')


@login_required
def notification_mark_all_read(request):
    """Mark all user's notifications as read."""
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    messages.success(request, 'All notifications marked as read.')
    return redirect('notifications:list')
