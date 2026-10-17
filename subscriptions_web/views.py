from django.shortcuts import render

from web_data import get_collection, load_data


def list_view(request):
    data = load_data()

    users = {
        user["id"]: user
        for user in get_collection(data, "users")
    }

    mailing_lists = {
        mailing_list["id"]: mailing_list
        for mailing_list in get_collection(data, "mailing_lists", "lists")
    }

    subscriptions = []

    for subscription in get_collection(data, "subscriptions"):
        user = users.get(subscription.get("user_id"))
        mailing_list = mailing_lists.get(subscription.get("list_id"))

        subscriptions.append({
            "user_name": user.get("name", "Неизвестный пользователь")
            if user else "Неизвестный пользователь",
            "list_name": mailing_list.get("name", "Неизвестный список")
            if mailing_list else "Неизвестный список",
        })

    return render(
        request,
        "subscriptions_web/list.html",
        {"subscriptions": subscriptions},
    )