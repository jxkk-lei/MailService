from collections import Counter

from django.shortcuts import render

from web_data import load_service, message_rows


def list_view(request):
    service = load_service()
    subscriber_counts = Counter(
        item.mailing_list.id for item in service.subscriptions
    )
    message_counts = Counter(
        item.mailing_list.id for item in service.messages
    )
    context = {
        "mailing_lists": [
            {
                "mailing_list": item,
                "subscriber_count": subscriber_counts[item.id],
                "message_count": message_counts[item.id],
            }
            for item in service.mailing_lists
        ],
    }
    return render(request, "mailing_lists_web/list.html", context)


def detail_view(request, list_id):
    service = load_service()
    mailing_list = next(
        (item for item in service.mailing_lists if item.id == list_id), None,
    )
    context = {
        "mailing_list": mailing_list,
        "subscribers": [
            item.user for item in service.subscriptions
            if item.mailing_list.id == list_id
        ],
        "messages": message_rows([
            item for item in service.messages
            if item.mailing_list.id == list_id
        ]),
    }
    return render(
        request, "mailing_lists_web/detail.html", context,
        status=404 if mailing_list is None else 200,
    )
