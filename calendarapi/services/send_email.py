from flask_mail import Message, Mail
from calendarapi.extensions import celery
from flask import current_app


@celery.task
def send_email(
    user_name,
    user_surname,
    user_email,
    appointment_date,
    appointment_time,
    lawyer_name,
    specialization_name,
    phone_number,
):
    lawyer_email_msg = Message(
        f"Нова зустріч. Клієнт {user_name } {user_surname}",
        recipients=[current_app.config["MAIL_DEFAULT_SENDER"]],
    )
    user_email_msg = Message(
        f"Нова зустріч. Юрист {lawyer_name}",
        recipients=[user_email],
    )
    user_email_msg.body = (
        f"Вітаю {user_name} {user_surname}!.\n"
        f"У вас заплановано зустріч на {appointment_date} за темою: {specialization_name}.\n"
        f"Юрист {lawyer_name} буде очікувати вас о {appointment_time} годині "
    )

    lawyer_email_msg.body = (
        f"Вітаю {lawyer_name}!.\n"
        f"{user_name} {user_surname} залишив(ла) заявку на отримання консультації за темою: {specialization_name}.\n"
        f"Зустріч заплановано на {appointment_date} о {appointment_time} годині."
        f"Телефон клієнта: {phone_number}"
    )

    mail = Mail()
    mail.send(user_email_msg)
    mail.send(lawyer_email_msg)

    return "Повідомлення відправлено"
