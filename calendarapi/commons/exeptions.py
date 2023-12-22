import os
from calendarapi.config import IMAGE_FORMATS, IMAGE_SIZE

# REQUIREMENTS
with open(os.path.join("calendarapi", "templates", "req_markup.html"), "r") as f:
    REQ_HTML_M = f.read()
REQ_PASSWORD = "Пароль повинен містити мінімум 1 спецсимвол (#$%^&+=!?), 1 цифру та 1 велику літеру. Усі літери повинні бути латиницею."
REQ_IMAGE = f"Розмір файлу не повинен перевищувати {IMAGE_SIZE} мб, підтримуються такі формати: {', '.join(IMAGE_FORMATS)}."
REQ_MAX_LEN = "Максимальна кількість символів - %s."


# GLOBAL
DATA_REQUIRED = "Це поле обов'язкове."
INVALID_EMAIL = "Невірний формат пошти."
INVALID_PASSWORD_LEN = "Довжина вашого пароля %s. Довжина пароля повинна бути мінімум 8 та максимум 64 символи."
INVALID_PASSWORD_EQ_LOGIN = "Пароль не повинен бути схожий на логін"
INVALID_EQUAL_PASSWORD = "Паролі повинні співпадати"
BAD_LOGIN_DATA = "Невірний логін або пароль"

# CONTACTS
IVNALID_COORDS = "Некоректні координати. Вкажіть число, яке менше або більше за 0"

# Admin USERS
EXPIRED_TOKEN = "Недійсний token"
NOT_FOUND_TOKEN = "Не знайдено аргумент: token"
ZERO_ACTIVE_USER = "Має залишитися хоча б один активний користувач"
LOSS_USER_CONTROL = (
    "Неможливо забрати доступ до керування обліковими записами у поточного користувача"
)
DELETE_CURRENT_USER = "Неможливо видалити поточного користувача"
USER_IS_NOT_ADMIN = "Користувач не адміністратор"
