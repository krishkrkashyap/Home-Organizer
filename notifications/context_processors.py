from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        qs = Notification.objects.filter(recipient=request.user)
        return {
            'unread_count': qs.filter(is_read=False).count(),
            'recent_notifications': qs[:5],
        }
    return {}
