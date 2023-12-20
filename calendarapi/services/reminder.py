# from datetime import datetime
# from typing import List

# from calendarapi.models import Appointment, Visitor
# from calendarapi.services.send_email import send_email
# from calendarapi.extensions import celery, db


# @celery.task()
# def check_appointments():
#     today = datetime.utcnow().date()

#     try:
#         appointments = (
#             db.session.query(
#                 Appointment.specialization,
#                 Appointment.appointment_date,
#                 Appointment.appointment_time,
#                 Appointment.lawyer,
#                 Visitor.name,
#                 Visitor.email,
#             )
#             .join(Visitor)
#             .filter(Appointment.appointment_date == today, Visitor.email.isnot(None))
#             .all()
#         )
#     except Exception as e:
#         return f"Виникла помилка при отриманні даних з БД. {e}"

#     if not appointments:
#         return "Записів на сьогодні не заплановано, або відсутні пошти для розсилки."

#     for appointment in appointments:
#         send_email.delay(
#             reminder=True,
#             visitor_name=appointment.name,
#             visitor_email=appointment.email,
#             specialization_name=appointment.specialization,
#             appointment_date=appointment.appointment_date,
#             appointment_time=str(appointment.appointment_time)[:-3],
#             lawyer_name=appointment.lawyer,
#         )
#     return "Листи з нагадуваннями надіслано."
