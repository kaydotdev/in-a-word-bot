from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class LoginForm(FlaskForm):
    Login = StringField("Login", [
        validators.DataRequired("Login cannot be empty!")
    ], render_kw={"placeholder": "Login"})

    Password = StringField("Password", [
        validators.DataRequired("Password cannot be empty!"),
        validators.Length("Password should contain at least 8 symbols!", min=8)
    ], render_kw={"placeholder": "Password"})

    Submit = SubmitField("Sign in")
