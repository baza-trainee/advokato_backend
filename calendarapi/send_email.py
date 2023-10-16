from flask_mail import Message, Mail


class Mailing:
    def __init__(self):
        self.user_mail = "aleshichevigor@yahoo.com"
        self.user_name = "Sergey"
        self.lawer_mail = "aleshichevigor@yahoo.com"
        self.lawer_name = "Djon"
        self.specialization = [
            "Цивільна",
            "Адміністративна",
            "Кримінальна",
        ]
        self.date = "25.08.2023"
        self.time = "12:00 - 13:00"

    def send_email(self):
        msg = Message(
            f"Нова зустріч. {self.user_name} зарегиструвався",
            sender="aleshichevigor@outlook.com",
            recipients=["aleshichevigor@yahoo.com"],
        )
        msg.body = f"Вітаю {self.lawer_name}! {self.user_name} зарегиструвався на {self.date} о {self.time} годині за темами {self.specialization}"
        Mail().send(msg)
        return "Повідомлення відправлено"


mailing_instance = Mailing()


mailing_instance.send_email()
