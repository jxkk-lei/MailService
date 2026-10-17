from django.shortcuts import render

from web_data import get_collection, load_data


def list_view(request):
    data = load_data()

    users = {
        user["id"]: user
        for user in get_collection(data, "users")
    }

    mailing_lists = []

    for mailing_list in get_collection(data, "mailing_lists", "lists"):
        owner = users.get(mailing_list.get("owner_id"))

        mailing_lists.append({
            "id": mailing_list.get("id"),
            "name": mailing_list.get("name", "Без названия"),
            "owner_name": owner.get("name", "Неизвестный пользователь")
            if owner else "Неизвестный пользователь",
        })

    return render(
        request,
        "mailing_lists_web/list.html",
        {"mailing_lists": mailing_lists},
    )