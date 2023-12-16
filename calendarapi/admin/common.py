import os
import uuid
from io import BytesIO

from flask import current_app, redirect, url_for, request, flash
import flask_login as login
from flask_admin import AdminIndexView, helpers, expose
from flask_admin.contrib.sqla import ModelView
from flask_mail import Message
from markupsafe import Markup
from wtforms import ValidationError, form, fields, validators
from werkzeug.datastructures.file_storage import FileStorage
from cloudinary import uploader

from calendarapi.config import IMAGE_FORMATS, IMAGE_SIZE
from calendarapi.extensions import db, mail
from calendarapi.models import User, UserSecurity
from calendarapi.models.user_permissions import Permission


class AdminModelView(ModelView):
    extra_css = ["/static/styles/green_mist.css"]

    create_modal = True
    edit_modal = True

    def is_accessible(self):
        return login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect("/admin/login")


def configure_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


class LoginForm(form.Form):
    login = fields.StringField(label="Логін", validators=[validators.InputRequired()])
    password = fields.PasswordField(
        label="Пароль", validators=[validators.InputRequired()]
    )

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError("Невірний логін")
        # we're comparing hashes
        if not user.password == user.hash_password(self.password.data):
            raise validators.ValidationError("Невірний пароль")

        if not user.is_active:
            raise validators.ValidationError("Користувач не адміністратор")

    def get_user(self):
        return db.session.query(User).filter_by(username=self.login.data).one_or_none()


class ForgotForm(form.Form):
    email = fields.EmailField(
        "email",
        validators=[
            validators.DataRequired(),
            validators.Email(),
        ],
    )


class PasswordResetForm(form.Form):
    password = fields.PasswordField("password", validators=[validators.DataRequired()])
    confirm_password = fields.PasswordField(
        "confirm password", validators=[validators.DataRequired()]
    )


class CustomAdminIndexView(AdminIndexView):
    extra_css = AdminModelView.extra_css

    def is_visible(self):
        # This view won't appear in the menu structure
        return False

    @expose("/", methods=("GET", "POST"))
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for(".login_view"))

        if db.session.query(Permission).count() < 1 and self.admin._views:
            permissions = [Permission(view_name="Усі розділи")]
            permissions += [
                Permission(view_name=admin_view.name)
                for admin_view in self.admin._views[1:]
            ]
            db.session.add_all(permissions)
            db.session.commit()
        return super(CustomAdminIndexView, self).index()

    @expose("/login/", methods=("GET", "POST"))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for(".index"))

        self._template_args["form"] = form
        return super(CustomAdminIndexView, self).index()

    @expose("/logout/")
    def logout_view(self):
        login.logout_user()
        return redirect(url_for(".index"))

    @expose("/forgot_password/", methods=["GET", "POST"])
    def forgot_password(self):
        if request.method == "POST":
            email = request.form.get("email")
            user = db.session.query(User).filter_by(email=email).one_or_none()
            if user:
                new_token = uuid.uuid4()
                user_security = (
                    db.session.query(UserSecurity)
                    .filter_by(user_id=user.id)
                    .one_or_none()
                )
                if user_security:
                    user_security.token = new_token
                else:
                    user_security = UserSecurity(user_id=user.id, token=new_token)
                    db.session.add(user_security)

                db.session.commit()

                text = f"Ви отримали цей лист через те, що зробили запит на перевстановлення пароля для облікового запису користувача на {request.host_url}admin"
                text += "\n\nБудь ласка, перейдіть на цю сторінку, та оберіть новий пароль: "
                text += f"\n{request.host_url}admin/reset_password/?token={user_security.token}\n"
                text += f"\nВаше користувацьке ім'я: {user.username}"
                text += "\n\nДякуємо за користування нашим сайтом!"

                message = Message(
                    "Відновлення доступу до Advocato-admin",
                    recipients=[user.email],
                    body=text,
                )
                mail.send(message=message)

            flash(
                "Якщо email вказано вірно, на нього буде відправлено повідомлення з інструкціями для відновлення доступу.",
                "success",
            )
            return redirect(f"{request.host_url}admin")
        else:
            form = ForgotForm(request.form)
            flash(
                f"Введіть ваш email, на який ми відправимо інструкції для відновлення доступу.",
                "info",
            )
            return self.render("admin/reset_password.html", form=form)

    @expose("/reset_password/", methods=["GET", "POST"])
    def reset_password(self):
        if request.method == "POST":
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            if password == confirm_password:
                token = request.args.get("token", default=None)
                if token:
                    user_security = (
                        db.session.query(UserSecurity)
                        .filter_by(token=token)
                        .one_or_none()
                    )
                    if user_security:
                        user = (
                            db.session.query(User)
                            .filter_by(id=user_security.user_id)
                            .one_or_none()
                        )
                        user.password = password
                        db.session.delete(user_security)
                        db.session.commit()
                        flash("Пароль успішно змінено.", "success")
                    else:
                        flash("Недійсний token", "error")
                else:
                    flash("Не знайдено аргумент: token", "error")
            else:
                flash("Паролі не співпадають", "error")
                return redirect(request.url)
        else:
            token = request.args.get("token", default=None)
            if token:
                user_security = (
                    db.session.query(UserSecurity).filter_by(token=token).one_or_none()
                )
                if user_security:
                    form = PasswordResetForm(request.form)
                    user = (
                        db.session.query(User)
                        .filter_by(id=user_security.user_id)
                        .one_or_none()
                    )
                    flash("Введіть новий пароль", "info")
                    return self.render("admin/reset_password.html", form=form)
                else:
                    flash("Недійсний token", "error")
            else:
                flash("Не знайдено аргумент: token", "error")

        return redirect(f"{request.host_url}admin")


def get_media_path(view_file_name: str):
    media_path = os.path.join(
        os.getcwd(), "calendarapi", "static", "media", view_file_name
    )
    return media_path


def custom_save_file(abs_media_path, file):
    if current_app.config["STORAGE"] == "STATIC":
        os.makedirs(abs_media_path, exist_ok=True)
        url_media_path = os.path.join(*abs_media_path.split(os.path.sep)[-3:])
        file_name = f'{uuid.uuid4().hex[:16]}.{file.filename.split(".")[-1]}'
        abs_file_path = os.path.join(abs_media_path, file_name)
        url_file_path = os.path.join(url_media_path, file_name)
        file.save(abs_file_path)
        return url_file_path
    else:
        upload_result = uploader.upload(file)
        return upload_result["url"]


def custom_delete_file(abs_media_path, file_path):
    if current_app.config["STORAGE"] == "STATIC":
        file_name = file_path.split(os.path.sep)[-1:][0]
        abs_file_path = os.path.join(abs_media_path, file_name)
        if os.path.exists(abs_file_path):
            os.remove(abs_file_path)


def validate_image(required: bool = True):
    def _validate_image(form, field):
        "validate image formats and image with IMAGE_FORMATS and IMAGE_SIZE from config"

        if required and not field.object_data and not field.data:
            raise ValidationError("Це поле обов'язкове.")
        if field.data:
            file_format = field.data.filename.split(".")[-1]
            if file_format not in IMAGE_FORMATS:
                raise ValidationError(
                    f"Формат файлу {file_format} не підтримується. Завантажте фото у наступних форматах: {', '.join(IMAGE_FORMATS)}."
                )
            buffer = field.data.stream.read()
            content_length = round(len(buffer) / 1024 / 1024, 2)
            if content_length > IMAGE_SIZE:
                raise ValidationError(
                    f"Розмір файлу {content_length} мб. перевищує максимально допустимий {IMAGE_SIZE} мб."
                )
            field.data = FileStorage(
                stream=BytesIO(buffer),
                content_length=content_length,
                content_type=field.data.content_type,
                filename=field.data.filename,
                name=field.data.name,
                headers=field.data.headers,
            )

    return _validate_image


def thumbnail_formatter(width: int = 240, field_name: str = "photo_path"):
    def _thumbnail_formatter(view, context, model, name):
        field_value = getattr(model, field_name)
        if not field_value:
            return ""

        if current_app.config["STORAGE"] == "STATIC":
            url = os.path.join(request.host_url, field_value)
        else:
            url = field_value

        if field_value.split(".")[-1] in current_app.config["IMAGE_FORMATS"]:
            return Markup(f"<img src={url} width={width}>")

    return _thumbnail_formatter


def format_text_as_markup(view, context, model, name):
    return Markup(getattr(model, name))
