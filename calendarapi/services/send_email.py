from flask_mail import Message, Mail
from calendarapi.models import Lawyer, Specialization
from calendarapi.extensions import celery


@celery.task
def send_email(
    user_name,
    user_surname,
    appointment_date,
    appointment_time,
    lawer_id,
    specialization_id,
    phone_number,
):
    lawer_name = Lawyer.query.filter_by(id=lawer_id).first()
    specialization = Specialization.query.filter_by(id=specialization_id).first()

    lawyer_email_msg = Message(
        f"Нова зустріч. {user_name } {user_surname} зарегиструвався",
        sender="aleshichevigor@outlook.com",
        recipients=["aleshichevigor@yahoo.com"],
    )

    user_email_msg = Message(
        f"Нова зустріч. Юрист {lawer_name}",
        sender="aleshichevigor@outlook.com",
        recipients=["aleshichevigor@yahoo.com"],
    )

    user_email_msg.body = (
        f"Вітаю {user_name} {user_surname}!.\n"
        f"У вас заплановано зустріч на {appointment_date} за темою: {specialization}.\n"
        f"Юрист {lawer_name} буде очікувати вас  о {appointment_time} годині "
    )

    lawyer_email_msg.body = (
        f"Вітаю {lawer_name}!.\n"
        f"{user_name} {user_surname} зарегиструвався на {appointment_date} о {appointment_time} годині за темою: {specialization}.\n"
        f"Телефон клієнта: {phone_number}"
    )

    mail = Mail()
    mail.send(user_email_msg)
    mail.send(lawyer_email_msg)

    return "Повідомлення відправлено"
