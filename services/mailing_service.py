from typing import Optional, Tuple

from models.mailing_list import MailingList
from models.message import Message
from models.subscription import Subscription
from models.user import User


class MailService:
    """Управляет пользователями, подписками и рассылками."""

    def __init__(
        self,
        users: Optional[list[User]] = None,
        mailing_lists: Optional[list[MailingList]] = None,
        subscriptions: Optional[list[Subscription]] = None,
        messages: Optional[list[Message]] = None,
    ) -> None:
        self.users = users or []
        self.mailing_lists = mailing_lists or []
        self.subscriptions = subscriptions or []
        self.messages = messages or []

    @staticmethod
    def _next_id(items: list) -> int:
        return max((item.id for item in items), default=0) + 1

    def get_user(self, user_id: int) -> User:
        for user in self.users:
            if user.id == user_id:
                return user
        raise ValueError("Пользователь не найден.")

    def get_mailing_list(self, list_id: int) -> MailingList:
        for mailing_list in self.mailing_lists:
            if mailing_list.id == list_id:
                return mailing_list
        raise ValueError("Список рассылки не найден.")

    def add_user(self, name: str) -> User:
        user = User(self._next_id(self.users), name)
        self.users.append(user)
        return user

    def add_mailing_list(self, name: str, owner_id: int) -> MailingList:
        owner = self.get_user(owner_id)
        mailing_list = MailingList(
            self._next_id(self.mailing_lists),
            name,
            owner,
        )
        self.mailing_lists.append(mailing_list)
        return mailing_list

    def subscribe(self, user_id: int, list_id: int) -> Subscription:
        user = self.get_user(user_id)
        mailing_list = self.get_mailing_list(list_id)

        for subscription in self.subscriptions:
            if (
                subscription.user.id == user_id
                and subscription.mailing_list.id == list_id
            ):
                raise ValueError("Пользователь уже подписан.")

        subscription = Subscription(user, mailing_list)
        self.subscriptions.append(subscription)
        return subscription

    def send_message(self, list_id: int, text: str) -> Tuple[Message, int]:
        mailing_list = self.get_mailing_list(list_id)
        subscribers = [
            subscription
            for subscription in self.subscriptions
            if subscription.mailing_list.id == list_id
        ]
        if not subscribers:
            raise ValueError("В списке нет подписчиков.")

        message = Message(
            self._next_id(self.messages),
            mailing_list,
            text,
        )
        self.messages.append(message)
        return message, len(subscribers)
