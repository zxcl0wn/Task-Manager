from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from user.middleware import get_current_user
from .models import Notification


@login_required(login_url='app_user:login')
def notifications_list(request):
    notifications = Notification.objects.filter(
        Q(user=get_current_user()) &
        Q(is_read=False)
    )

    context = {
        'notifications': notifications,
    }

    for notification in notifications:
        notification.is_read = True
        notification.save()

    return render(request, 'notification/notifications_list.html', context=context)
