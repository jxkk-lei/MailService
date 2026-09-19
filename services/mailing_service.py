from datetime import date


def send_message(user, mailing_list, message, subscribers):
    if subscribers <= 0:
        print("Невозможно отправить рассылку: нет подписчиков.")
        return

    if message.text == "":
        print("Невозможно отправить рассылку: сообщение пустое.")
        return

    print("\nРассылка отправлена!")
    print("Автор:", user.username)
    print("Рассылка:", mailing_list.name)
    print("Получателей:", subscribers)
    print("Сообщение:", message.text)
    print("Дата отправки:", date.today())