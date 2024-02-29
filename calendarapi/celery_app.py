from celery.schedules import crontab

from calendarapi.app import init_celery


app = init_celery()
app.conf.imports = app.conf.imports + (
    "calendarapi.tasks.example",
    "calendarapi.services.send_email",
    "calendarapi.services.reminder",
)

app.conf.beat_schedule = {
    "every_day_at_8_am": {
        "task": "calendarapi.services.reminder.check_appointments",
        "schedule": crontab(hour=6, minute=0),
    }
}
