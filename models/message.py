from datetime import date
from typing import Optional

from models.mailing_list import MailingList


class Message:
    """Сообщение, созданное для списка рассылки."""

    def __init__(
        self,
        message_id: int,
        mailing_list: MailingList,
        text: str,
        sent_date: Optional[str] = None,
    ) -> None:
        if not text.strip():
            raise ValueError("Сообщение не может быть пустым.")
        self.id = message_id
        self.mailing_list = mailing_list
        self.text = text.strip()
        self.date = sent_date or date.today().isoformat()

    def __str__(self) -> str:
        return (
            f"{self.id}. Список: {self.mailing_list.name}; "
            f"{self.text}; {self.date}"
        )
