"""Загрузка существующей объектной модели для веб-представлений."""

import logging
from datetime import date
from pathlib import Path

from services.mailing_service import MailService
from storage.json_storage import JsonStorage

DATA_FILE = Path(__file__).resolve().parent / "data" / "mailservice.json"
logger = logging.getLogger(__name__)


def load_service():
    """Читать JSON через хранилище ПР3, не создавая файл при GET-запросе."""
    if not DATA_FILE.exists():
        return MailService()

    try:
        return JsonStorage(DATA_FILE).load()
    except ValueError as error:
        logger.warning("Не удалось прочитать данные MailService: %s", error)
        return MailService()


def message_rows(messages):
    """Подготовить даты к фильтру date без изменения объектов Message."""
    rows = []
    for message in messages:
        try:
            sent_date = date.fromisoformat(message.date)
        except (TypeError, ValueError):
            sent_date = None
        rows.append({"message": message, "sent_date": sent_date})
    return rows
