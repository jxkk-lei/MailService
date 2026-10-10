class User:
    """Пользователь сервиса рассылок."""

    def __init__(self, user_id: int, name: str) -> None:
        if not name.strip():
            raise ValueError("Имя пользователя не может быть пустым.")
        self.id = user_id
        self.name = name.strip()

    def __str__(self) -> str:
        return f"{self.id}. {self.name}"
