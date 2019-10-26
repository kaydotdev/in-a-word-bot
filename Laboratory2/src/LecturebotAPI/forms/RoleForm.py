from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, StringField, SubmitField, validators


class RoleForm(FlaskForm):
    id = HiddenField("Id")

    Name = StringField("Role name: ", [
        validators.DataRequired("Role name cannot be empty!")
    ], render_kw={"placeholder": "Name: "})

    Priority = IntegerField("Role priority: ", [
        validators.DataRequired("Role priority cannot be empty!")
    ], render_kw={"placeholder": "Priority: "})

    Submit = SubmitField("Add")
