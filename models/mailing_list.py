from models.user import User


class MailingList:
    """Список рассылки, принадлежащий пользователю."""

    def __init__(
        self,
        list_id: int,
        name: str,
        owner: User,
    ) -> None:
        if not name.strip():
            raise ValueError("Название списка не может быть пустым.")
        self.id = list_id
        self.name = name.strip()
        self.owner = owner

    def __str__(self) -> str:
        return f"{self.id}. {self.name} (автор: {self.owner.name})"
