from models.user import create_user
from models.mailing_list import create_mailing_list
from models.message import create_message


def get_next_id(items: list[dict]) -> int:
    if not items:
        return 1

    return max(item["id"] for item in items) + 1


def add_user(data: dict, name: str) -> None:
    if not name.strip():
        raise ValueError("Имя пользователя не может быть пустым.")

    user = create_user(
        get_next_id(data["users"]),
        name.strip(),
    )
    data["users"].append(user)


def add_mailing_list(
    data: dict,
    name: str,
    owner_id: int
) -> None:
    if not name.strip():
        raise ValueError("Название списка не может быть пустым.")

    if not any(
        user["id"] == owner_id
        for user in data["users"]
    ):
        raise ValueError("Пользователь не найден.")

    mailing_list = create_mailing_list(
        get_next_id(data["mailing_lists"]),
        name.strip(),
        owner_id,
    )
    data["mailing_lists"].append(mailing_list)


def subscribe(
    data: dict,
    user_id: int,
    list_id: int
) -> None:
    user_exists = any(
        user["id"] == user_id
        for user in data["users"]
    )
    list_exists = any(
        mailing_list["id"] == list_id
        for mailing_list in data["mailing_lists"]
    )

    if not user_exists:
        raise ValueError("Пользователь не найден.")

    if not list_exists:
        raise ValueError("Список рассылки не найден.")

    for subscription in data["subscriptions"]:
        if (
            subscription["user_id"] == user_id
            and subscription["list_id"] == list_id
        ):
            raise ValueError("Пользователь уже подписан.")

    data["subscriptions"].append({
        "user_id": user_id,
        "list_id": list_id,
    })


def send_message(
    data: dict,
    list_id: int,
    text: str
) -> int:
    mailing_list = next(
        (
            item for item in data["mailing_lists"]
            if item["id"] == list_id
        ),
        None,
    )

    if mailing_list is None:
        raise ValueError("Список рассылки не найден.")

    if not text.strip():
        raise ValueError("Сообщение не может быть пустым.")

    subscribers = [
        item for item in data["subscriptions"]
        if item["list_id"] == list_id
    ]

    if not subscribers:
        raise ValueError("В списке нет подписчиков.")

    message = create_message(
        get_next_id(data["messages"]),
        list_id,
        text.strip(),
    )
    data["messages"].append(message)

    return len(subscribers)