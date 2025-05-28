from django.shortcuts import render


def notifications_list(request):
    context = {

    }

    return render(request, 'notification/notifications_list.html', context=context)