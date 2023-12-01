from flask import redirect, url_for, request
import flask_login as login
from flask_admin import AdminIndexView, helpers, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import form, fields, validators

from calendarapi.extensions import db, pwd_context
from calendarapi.models import User


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
        "Введіть ваш e-mail", validators=[validators.DataRequired(), validators.Email(),], 
    )

class PasswordResetForm(form.Form):
    new_password = fields.PasswordField("Password", validators=[validators.DataRequired()], render_kw={'placeholder': 'Ваш новий текст'}
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

    @expose("/forgot_password/", methods=['GET', 'POST'])
    def forgot_password(self):
        if request.method == 'POST':
            email=request.form.get('email')
            record = db.session.query(User).filter_by(email=email).one_or_none()
            if record:
                return record.id
            else:
                return f"емейл {email} не знайдено"
        # модель бд id : token
        # коли користувач вводить емейл отримує посилання
        form = ForgotForm(request.form)
        return self.render("admin/reset_password.html", form=form)
