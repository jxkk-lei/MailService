from django.shortcuts import render

from web_data import get_collection, load_data


def list_view(request):
    data = load_data()

    mailing_lists = {
        mailing_list["id"]: mailing_list
        for mailing_list in get_collection(data, "mailing_lists", "lists")
    }

    messages = []

    for message in get_collection(data, "messages"):
        mailing_list = mailing_lists.get(message.get("list_id"))

        messages.append({
            "id": message.get("id"),
            "text": message.get("text", ""),
            "date": message.get("date", ""),
            "list_name": mailing_list.get("name", "Неизвестный список")
            if mailing_list else "Неизвестный список",
        })

    return render(
        request,
        "messages_web/list.html",
        {"messages": messages},
    )