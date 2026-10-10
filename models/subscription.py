from models.mailing_list import MailingList
from models.user import User


class Subscription:
    """Связь подписчика со списком рассылки."""

    def __init__(
        self,
        user: User,
        mailing_list: MailingList,
    ) -> None:
        self.user = user
        self.mailing_list = mailing_list

    def __str__(self) -> str:
        return (
            f"{self.user.name} подписан на "
            f"«{self.mailing_list.name}»"
        )
