# from datetime import datetime
# from typing import List

# from calendarapi.models import Appointment, Visitor, Lawyer, Specialization
# from calendarapi.services.send_email import send_email
# from calendarapi.extensions import celery


# @celery.task()
# def check_appointments():
#     today = datetime.utcnow().date()

#     try:
#         appointments: List[Appointment] = Appointment.query.filter(
#             Appointment.appointment_date == today
#         ).all()
#     except Exception as e:
#         return f"Виникла помилка при отриманні даних з БД. {e}"

#     if not appointments:
#         return "Записів на сьогодні не заплановано."

#     for appointment in appointments:
#         visitor: Visitor = Visitor.query.get(appointment.visitor_id)
#         lawyer: Lawyer = Lawyer.query.get(appointment.lawyer_id)
#         specialization: Specialization = Specialization.query.get(
#             appointment.specialization_id
#         )
#         if all([visitor, lawyer, specialization]):
#             send_email.delay(
#                 reminder=True,
#                 visitor_name=visitor.name,
#                 visitor_email=visitor.email,
#                 specialization_name=specialization.specialization_name,
#                 appointment_date=appointment.appointment_date,
#                 appointment_time=str(appointment.appointment_time)[:-3],
#                 lawyer_name=lawyer.name,
#             )
#     return "Листи з нагадуваннями надіслано."
