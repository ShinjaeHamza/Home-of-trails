from .models import Notification

def unread_notifications(request):
    if request.user.is_authenticated:
        unread = Notification.objects.filter(user=request.user, is_read=False)
        return {'unread_notifications': unread}
    return {'unread_notifications': []}


def notifications_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        return {'notifications': notifications}
    return {'notifications': []}
