from django.shortcuts import render

from web_data import load_service, message_rows


def list_view(request):
    service = load_service()
    context = {"messages": message_rows(service.messages)}
    return render(request, "messages_web/list.html", context)


def detail_view(request, message_id):
    service = load_service()
    message = next(
        (item for item in service.messages if item.id == message_id), None,
    )
    context = (
        message_rows([message])[0] if message is not None
        else {"message": None, "sent_date": None}
    )
    return render(
        request, "messages_web/detail.html", context,
        status=404 if message is None else 200,
    )
