from django.shortcuts import render

from web_data import load_service


def list_view(request):
    service = load_service()
    return render(
        request, "subscriptions_web/list.html",
        {"subscriptions": service.subscriptions},
    )
