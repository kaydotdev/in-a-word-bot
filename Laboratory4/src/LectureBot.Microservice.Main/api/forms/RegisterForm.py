from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, HiddenField, PasswordField


class RegisterForm(FlaskForm):
    id = HiddenField("Id")

    Login = StringField("Login", [
        validators.DataRequired("Login cannot be empty!")
    ], render_kw={"placeholder": "Login", "id": "inputLogin"})

    Password = PasswordField("Password", [
        validators.DataRequired("Password cannot be empty!"),
        validators.Length(min=8, message="Password should contain at least 8 symbols!")
    ], render_kw={"placeholder": "Password", "id": "inputPassword"})

    ConfirmPassword = PasswordField("ConfirmPassword", [
        validators.DataRequired("Password cannot be empty!"),
        validators.Length(min=8, message="Password should contain at least 8 symbols!")
    ], render_kw={"placeholder": "Password", "id": "inputPasswordConfirm"})

    Submit = SubmitField("Sign up")
