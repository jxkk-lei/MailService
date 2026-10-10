import pytest

from services.mailing_service import (
    add_user,
    add_mailing_list,
    subscribe,
    send_message,
)


def create_test_data() -> dict:
    return {
        "users": [],
        "mailing_lists": [],
        "subscriptions": [],
        "messages": [],
    }


def test_create_mailing_and_send_message() -> None:
    data = create_test_data()

    add_user(data, "Алексей")
    add_mailing_list(data, "Новости", 1)
    subscribe(data, 1, 1)

    count = send_message(data, 1, "Привет!")

    assert count == 1
    assert len(data["messages"]) == 1


def test_empty_message() -> None:
    data = create_test_data()

    add_user(data, "Алексей")
    add_mailing_list(data, "Новости", 1)
    subscribe(data, 1, 1)

    with pytest.raises(ValueError):
        send_message(data, 1, "")


def test_duplicate_subscription() -> None:
    data = create_test_data()

    add_user(data, "Алексей")
    add_mailing_list(data, "Новости", 1)
    subscribe(data, 1, 1)

    with pytest.raises(ValueError):
        subscribe(data, 1, 1)