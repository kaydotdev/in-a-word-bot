from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, validators


class ResourceForm(FlaskForm):
    URL = StringField("URL: ", [
        validators.DataRequired("URL cannot be empty!")
    ])

    Description = StringField("Description: ", [
        validators.DataRequired("Description cannot be empty!")
    ])

    submit = SubmitField("Add")