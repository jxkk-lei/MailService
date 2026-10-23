from django.shortcuts import render

from web_data import load_service


def list_view(request):
    service = load_service()
    return render(request, "users_web/list.html", {"users": service.users})


def detail_view(request, user_id):
    service = load_service()
    user = next((u for u in service.users if u.id == user_id), None)
    context = {
        "profile": user,
        "mailing_lists": [
            item for item in service.mailing_lists if item.owner.id == user_id
        ],
        "subscriptions": [
            item for item in service.subscriptions if item.user.id == user_id
        ],
    }
    return render(
        request, "users_web/detail.html", context,
        status=404 if user is None else 200,
    )
