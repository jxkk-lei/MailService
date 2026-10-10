from datetime import date


def create_message(
    message_id: int,
    list_id: int,
    text: str
) -> dict:
    return {
        "id": message_id,
        "list_id": list_id,
        "text": text,
        "date": date.today().isoformat(),
    }