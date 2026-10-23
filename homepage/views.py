from django.shortcuts import render

from web_data import load_service


def index(request):
    service = load_service()
    context = {
        "users": service.users,
        "mailing_lists": service.mailing_lists,
        "messages": service.messages,
        "subscriptions": service.subscriptions,
    }
    return render(request, "homepage/index.html", context)


def not_found(request, exception=None):
    return render(request, "404.html", status=404)
