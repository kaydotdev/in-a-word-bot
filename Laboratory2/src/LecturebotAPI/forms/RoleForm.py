from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, validators


class RoleForm(FlaskForm):
    Name = StringField("Role name: ", [
        validators.DataRequired("Role name cannot be empty!")
    ])

    Priority = IntegerField("Role priority: ", [
        validators.DataRequired("Role priority cannot be empty!")
    ])

    submit = SubmitField("Add")
