from services.mailing_service import MailService
from storage.json_storage import JsonStorage


def show_data(service: MailService) -> None:
    print("\nПользователи:")
    for user in service.users:
        print(user)

    print("\nСписки рассылок:")
    for mailing_list in service.mailing_lists:
        print(mailing_list)

    print("\nПодписки:")
    for subscription in service.subscriptions:
        print(subscription)

    print("\nСообщения:")
    for message in service.messages:
        print(message)


def main() -> None:
    storage = JsonStorage()
    try:
        service = storage.load()
    except (ValueError, OSError) as error:
        print(f"Ошибка загрузки данных: {error}")
        return

    while True:
        print("\n=== MailService ===")
        print("1. Добавить пользователя")
        print("2. Создать список рассылки")
        print("3. Подписать пользователя")
        print("4. Отправить сообщение")
        print("5. Просмотреть данные")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                name = input("Имя пользователя: ")
                user = service.add_user(name)
                storage.save(service)
                print(f"Пользователь добавлен: {user}")

            elif choice == "2":
                name = input("Название списка: ")
                owner_id = int(input("ID автора: "))
                mailing_list = service.add_mailing_list(name, owner_id)
                storage.save(service)
                print(f"Список создан: {mailing_list}")

            elif choice == "3":
                user_id = int(input("ID пользователя: "))
                list_id = int(input("ID списка: "))
                subscription = service.subscribe(user_id, list_id)
                storage.save(service)
                print(f"Подписка оформлена: {subscription}")

            elif choice == "4":
                list_id = int(input("ID списка: "))
                message_text = input("Текст сообщения: ")
                message, count = service.send_message(list_id, message_text)
                storage.save(service)
                print(f"Сообщение сохранено и отправлено {count} подписчикам.")
                print(message)

            elif choice == "5":
                show_data(service)

            elif choice == "0":
                print("Работа MailService завершена.")
                break

            else:
                print("Неизвестная команда.")

        except (ValueError, KeyError) as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
