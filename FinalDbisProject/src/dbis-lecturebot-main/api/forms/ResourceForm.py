from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class ResourceForm(FlaskForm):
    URL = StringField("URL: ", [
        validators.DataRequired("URL cannot be empty!")
    ], render_kw={"placeholder": "URL: "})

    Description = StringField("Description: ", [
        validators.DataRequired("Description cannot be empty!")
    ], render_kw={"placeholder": "Description: "})

    Submit = SubmitField("Add")
