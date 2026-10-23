import pytest

from models.mailing_list import MailingList
from models.message import Message
from models.subscription import Subscription
from models.user import User
from services.mailing_service import MailService
from storage.json_storage import JsonStorage


def test_user_and_mailing_list_objects() -> None:
    user = User(1, "Алексей")
    mailing_list = MailingList(1, "Новости", user)

    assert user.name == "Алексей"
    assert mailing_list.owner is user
    assert "Новости" in str(mailing_list)


def test_create_subscription_and_send_message() -> None:
    service = MailService()
    service.add_user("Алексей")
    service.add_user("Мария")
    service.add_mailing_list("Новости", 1)
    service.subscribe(1, 1)
    service.subscribe(2, 1)

    message, count = service.send_message(1, "Привет!")

    assert isinstance(message, Message)
    assert count == 2
    assert len(service.messages) == 1


def test_empty_message_is_rejected() -> None:
    service = MailService()
    service.add_user("Алексей")
    service.add_mailing_list("Новости", 1)
    service.subscribe(1, 1)

    with pytest.raises(ValueError, match="пустым"):
        service.send_message(1, "  ")


def test_duplicate_subscription_is_rejected() -> None:
    service = MailService()
    service.add_user("Алексей")
    service.add_mailing_list("Новости", 1)
    service.subscribe(1, 1)

    with pytest.raises(ValueError, match="уже подписан"):
        service.subscribe(1, 1)


def test_json_round_trip_restores_objects(tmp_path) -> None:
    path = tmp_path / "mailservice.json"
    storage = JsonStorage(path)
    service = MailService()
    service.add_user("Алексей")
    service.add_mailing_list("Новости", 1)
    service.subscribe(1, 1)
    service.send_message(1, "Тестовое сообщение")

    storage.save(service)
    loaded = storage.load()

    assert isinstance(loaded.users[0], User)
    assert isinstance(loaded.mailing_lists[0], MailingList)
    assert isinstance(loaded.subscriptions[0], Subscription)
    assert isinstance(loaded.messages[0], Message)
    assert loaded.subscriptions[0].user is loaded.users[0]
    assert loaded.messages[0].mailing_list is loaded.mailing_lists[0]
    assert loaded.messages[0].text == "Тестовое сообщение"


def test_invalid_json_raises_value_error(tmp_path) -> None:
    path = tmp_path / "mailservice.json"
    path.write_text("{broken json", encoding="utf-8")

    with pytest.raises(ValueError, match="загрузить"):
        JsonStorage(path).load()
