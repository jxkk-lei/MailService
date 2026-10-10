import json
from pathlib import Path

DATA_FILE = Path("data/mailservice.json")


def load_data() -> dict:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        return {
            "users": [],
            "mailing_lists": [],
            "subscriptions": [],
            "messages": [],
        }

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        raise ValueError(
            "Не удалось загрузить данные проекта."
        ) from error

    return data


def save_data(data: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )
    except OSError as error:
        raise ValueError(
            "Не удалось сохранить данные проекта."
        ) from error