from storage.json_storage import load_data, save_data
from services.mailing_service import (
    add_user,
    add_mailing_list,
    subscribe,
    send_message,
)


def show_data(data: dict) -> None:
    print("\nПользователи:")
    for user in data["users"]:
        print(f'{user["id"]}. {user["name"]}')

    print("\nСписки рассылок:")
    for mailing_list in data["mailing_lists"]:
        print(
            f'{mailing_list["id"]}. '
            f'{mailing_list["name"]} '
            f'(автор: {mailing_list["owner_id"]})'
        )

    print("\nСообщения:")
    for message in data["messages"]:
        print(
            f'{message["id"]}. '
            f'Список: {message["list_id"]}; '
            f'{message["text"]}; '
            f'{message["date"]}'
        )


def main() -> None:
    try:
        data = load_data()
    except ValueError as error:
        print(error)
        return

    while True:
        print("\n=== MailService ===")
        print("1. Добавить пользователя")
        print("2. Создать список рассылки")
        print("3. Подписать пользователя")
        print("4. Отправить сообщение")
        print("5. Просмотреть данные")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                name = input("Имя пользователя: ")
                add_user(data, name)
                save_data(data)
                print("Пользователь добавлен.")

            elif choice == "2":
                name = input("Название списка: ")
                owner_id = int(input("ID автора: "))
                add_mailing_list(data, name, owner_id)
                save_data(data)
                print("Список рассылки создан.")

            elif choice == "3":
                user_id = int(input("ID пользователя: "))
                list_id = int(input("ID списка: "))
                subscribe(data, user_id, list_id)
                save_data(data)
                print("Подписка оформлена.")

            elif choice == "4":
                list_id = int(input("ID списка: "))
                text = input("Текст сообщения: ")
                count = send_message(data, list_id, text)
                save_data(data)
                print(f"Сообщение отправлено {count} подписчикам.")

            elif choice == "5":
                show_data(data)

            elif choice == "0":
                print("Работа MailService завершена.")
                break

            else:
                print("Неизвестная команда.")

        except ValueError as error:
            print("Ошибка:", error)


if __name__ == "__main__":
    main()