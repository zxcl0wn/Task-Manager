from django.shortcuts import render
from .models import Notification


def notifications_list(request):
    notifications = Notification.objects.all()
    context = {
        'notifications': notifications,
    }

    return render(request, 'notification/notifications_list.html', context=context)