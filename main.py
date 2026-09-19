from models.user import User
from models.mailing_list import MailingList
from models.message import Message
from services.mailing_service import send_message


print("=== MailFlow ===")
print("Создание рассылки")

username = input("Введите имя пользователя: ")
mailing_name = input("Введите название рассылки: ")
subscribers = int(input("Введите количество подписчиков: "))
message_text = input("Введите сообщение: ")

user = User(username)
mailing_list = MailingList(mailing_name)
message = Message(message_text)

send_message(
    user,
    mailing_list,
    message,
    subscribers
)