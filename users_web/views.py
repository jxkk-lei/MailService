from django.shortcuts import render

from web_data import get_collection, load_data


def list_view(request):
    data = load_data()
    users = get_collection(data, "users")

    return render(
        request,
        "users_web/list.html",
        {"users": users},
    )