import json
from pathlib import Path
from typing import Any

from models.mailing_list import MailingList
from models.message import Message
from models.subscription import Subscription
from models.user import User
from services.mailing_service import MailService


class JsonStorage:
    """Загружает и сохраняет объектную модель MailService в JSON."""

    def __init__(self, path: str | Path = "data/mailservice.json") -> None:
        self.path = Path(path)

    def save(self, service: MailService) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data: dict[str, Any] = {
            "users": [
                {"id": user.id, "name": user.name}
                for user in service.users
            ],
            "mailing_lists": [
                {
                    "id": mailing_list.id,
                    "name": mailing_list.name,
                    "owner_id": mailing_list.owner.id,
                }
                for mailing_list in service.mailing_lists
            ],
            "subscriptions": [
                {
                    "user_id": subscription.user.id,
                    "list_id": subscription.mailing_list.id,
                }
                for subscription in service.subscriptions
            ],
            "messages": [
                {
                    "id": message.id,
                    "list_id": message.mailing_list.id,
                    "text": message.text,
                    "date": message.date,
                }
                for message in service.messages
            ],
        }
        try:
            with self.path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as error:
            raise ValueError("Не удалось сохранить данные проекта.") from error

    def load(self) -> MailService:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            service = MailService()
            self.save(service)
            return service

        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            raise ValueError("Не удалось загрузить данные проекта.") from error

        try:
            users_by_id = {
                item["id"]: User(item["id"], item["name"])
                for item in data.get("users", [])
            }
            mailing_lists_by_id = {
                item["id"]: MailingList(
                    item["id"],
                    item["name"],
                    users_by_id[item["owner_id"]],
                )
                for item in data.get("mailing_lists", [])
            }
            subscriptions = [
                Subscription(
                    users_by_id[item["user_id"]],
                    mailing_lists_by_id[item["list_id"]],
                )
                for item in data.get("subscriptions", [])
            ]
            messages = [
                Message(
                    item["id"],
                    mailing_lists_by_id[item["list_id"]],
                    item["text"],
                    item.get("date"),
                )
                for item in data.get("messages", [])
            ]
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(
                "Файл данных имеет неправильную структуру."
            ) from error

        return MailService(
            users=list(users_by_id.values()),
            mailing_lists=list(mailing_lists_by_id.values()),
            subscriptions=subscriptions,
            messages=messages,
        )
