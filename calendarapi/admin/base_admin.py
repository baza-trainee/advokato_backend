from re import search
import uuid

from flask import current_app, redirect, url_for, request, flash
import flask_login as login
from flask_admin import AdminIndexView, helpers, expose
from flask_admin.contrib.sqla import ModelView
from flask_mail import Message
from wtforms import form, fields, validators

from calendarapi.extensions import db, mail
from calendarapi.models import User, UserSecurity
from calendarapi.models.user_permissions import Permission
from calendarapi.commons.exeptions import (
    INVALID_EQUAL_PASSWORD,
    BAD_LOGIN_DATA,
    DATA_REQUIRED,
    EXPIRED_TOKEN,
    INVALID_PASSWORD_EQ_LOGIN,
    INVALID_PASSWORD_LEN,
    NOT_FOUND_TOKEN,
    REQ_PASSWORD,
    USER_IS_NOT_ADMIN,
)


class AdminModelView(ModelView):
    extra_css = ["/static/styles/green_mist.css"]

    create_modal = True
    edit_modal = True

    def is_accessible(self):
        permissions = []
        PERMISSION_ALL = current_app.config["PERMISSION_ALL"]
        if not login.current_user.is_anonymous:
            permissions += [
                permision.view_name for permision in login.current_user.permissions
            ]
        return login.current_user.is_authenticated and (
            PERMISSION_ALL in permissions or self.name in permissions
        )

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
        label="Пароль", validators=[validators.InputRequired(message=DATA_REQUIRED)]
    )

    def validate_login(self, field):
        user = self.get_user()

        if user is None or not user.password == user.hash_password(self.password.data):
            raise validators.ValidationError(message=BAD_LOGIN_DATA)

        if not user.is_active:
            raise validators.ValidationError(message=USER_IS_NOT_ADMIN)

    def get_user(self):
        return db.session.query(User).filter_by(username=self.login.data).one_or_none()


class ForgotForm(form.Form):
    email = fields.EmailField(
        "email",
        validators=[
            validators.DataRequired(message=DATA_REQUIRED),
            validators.Email(),
        ],
    )


class PasswordResetForm(form.Form):
    password = fields.PasswordField(
        "password", validators=[validators.DataRequired(message=DATA_REQUIRED)]
    )
    confirm_password = fields.PasswordField(
        "confirm password", validators=[validators.DataRequired(message=DATA_REQUIRED)]
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

        if db.session.query(Permission).count() < 2 and self.admin._views:
            permissions = [
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
        self.base_url = current_app.config.get("BASE_URL")
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

                text = f"Ви отримали цей лист через те, що зробили запит на перевстановлення пароля для облікового запису користувача на {current_app.config.get('BASE_URL')}/admin"
                text += "\n\nБудь ласка, перейдіть на цю сторінку, та оберіть новий пароль: "
                text += f"\n{current_app.config.get('BASE_URL')}/admin/reset_password/?token={user_security.token}\n"
                text += f"\nВаше користувацьке ім'я: {user.username}"
                text += "\n\nДякуємо за користування нашим сайтом!"

                message = Message(
                    "Відновлення доступу до Status-AC-Admin",
                    recipients=[user.email],
                    body=text,
                )
                mail.send(message=message)

            flash(
                "Якщо email вказано вірно, на нього буде відправлено повідомлення з інструкціями для відновлення доступу.",
                "success",
            )
            return redirect(f"{current_app.config.get('BASE_URL')}/admin")
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
            validation_ok = False
            if password == confirm_password:
                password_len = len(password)
                regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!])[A-Za-z\d@#$%^&+=!?]*$"
                if not 8 <= password_len <= 64:
                    flash(
                        f"{INVALID_PASSWORD_LEN % password_len} {REQ_PASSWORD}",
                        "error",
                    )
                elif not search(regex, password):
                    flash(REQ_PASSWORD, "error")
                else:
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
                            if user.username.lower() in password.lower():
                                flash(INVALID_PASSWORD_EQ_LOGIN, "error")
                            else:
                                validation_ok = True
                                user.password = password
                                db.session.delete(user_security)
                                db.session.commit()
                                flash("Пароль успішно змінено.", "success")
                        else:
                            flash(EXPIRED_TOKEN, "error")
                    else:
                        flash(NOT_FOUND_TOKEN, "error")

            if not validation_ok:
                flash(INVALID_EQUAL_PASSWORD, "error")
                return redirect(
                    f"{current_app.config.get('BASE_URL')}/{'/'.join(request.url.split('/')[-3:])}"
                )
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
                    flash(EXPIRED_TOKEN, "error")
            else:
                flash(NOT_FOUND_TOKEN, "error")

        return redirect(f"{current_app.config.get('BASE_URL')}/admin")
