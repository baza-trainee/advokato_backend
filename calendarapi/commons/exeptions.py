from calendarapi.config import IMAGE_FORMATS, IMAGE_SIZE

# REQUIREMENTS
REQ_HTML_M = """<hr>
<details><summary><b>Можна використовувати HTML теги для форматування тексту.</b></summary>
<ul>
  <li><h5 style="display: inline;">&lt;h5&gt;Заголовок рівня 5&lt;/h5&gt;(Розміри від 1 до 6)</h5></li>
  <li><p style="display: inline; margin-left: 20px;">&lt;p&gt;Абзац тексту&lt;/p&gt;</p></li>
  <li style="text-align: center">&lt;center&gt;текст по центру&lt;/center&gt;</li>
  <li><span>&lt;span&gt;Звичайний текстовий блок без абзацу.&lt;/span&gt;</span></li>
  <li>&lt;b&gt;<b>жирний</b>&lt;/b&gt; &lt;i&gt;<i>курсивний</i>&lt;/i&gt; &lt;u&gt;<u>підкреслений</u>&lt;/u&gt; &lt;s&gt;<s>закреслений</s>&lt;/s&gt;</li></ul>
<h6><b>Теги для форматування можна комбінувати:</b></h6>
<p>&lt;p&gt;&lt;b&gt;<b>Абзац тексту жирним</b>&lt;/b&gt; та &lt;i&gt;<i>курсивом</i>&lt;/i&gt;<br>&lt;br&gt;новий рядок у першому абзаці. Кінець першого абзацу, закриваємо тег абзацу.&lt;/p&gt;</p>
<ul>&lt;ul&gt;Заголовок ненумерованого списку<li>&lt;li&gt;перший елемент&lt;/li&gt;</li><li>&lt;li&gt;другий елемент&lt;/li&gt; закриваємо тег списку &lt;/ul&gt;</li></ul>
<span>&lt;span&gt;Звичайний текстовий блок без абзацу.<br>&lt;br&gt;новий рядок у тегу span. Закриваємо текстовий блок.&lt;/span&gt;</span>
<ol>&lt;ol&gt;Заголовок нумерованого списку<li>&lt;li&gt;перший елемент&lt;/li&gt;</li><li>&lt;li&gt;другий елемент&lt;/li&gt; закриваємо тег списку &lt;/ol&gt;</li></ol>
</details><hr>"""
REQ_PASSWORD = "Пароль повинен містити мінімум 1 спецсимвол (#$%^&+=!?), 1 цифру та 1 велику літеру. Всі літери повинні бути латиницею."
REQ_IMAGE = f"Розмір файлу не повинен перевищувати {IMAGE_SIZE} мб, підтримуються такі формати: {', '.join(IMAGE_FORMATS)}."
REQ_MAX_LEN = "Максимальна кількість символів - %s."


# GLOBAL
DATA_REQUIRED = "Це поле обов'язкове."
INVALID_EMAIL = "Невірний формат пошти."
INVALID_PASSWORD_LEN = "Ви ввели %s символів. Довжина пароля повинна бути мінімум 8 та максимум 64 символи."
INVALID_EQUAL_PASSWORD = "Паролі повинні співпадати"
BAD_LOGIN_DATA = "Невірний логін або пароль"

# CONTACTS
IVNALID_COORDS = "Невірний формат для координат. Приймаються лише числа."

# Admin USERS
EXPIRED_TOKEN = "Недійсний token"
NOT_FOUND_TOKEN = "Не знайдено аргумент: token"
ZERO_ACTIVE_USER = "Має залишитися хоча б один активний користувач"
LOSS_USER_CONTROL = (
    "Неможливо забрати доступ до керування обліковими записами у поточного користувача"
)
DELETE_CURRENT_USER = "Неможливо видалити поточного користувача"
USER_IS_NOT_ADMIN = "Користувач не адміністратор"
