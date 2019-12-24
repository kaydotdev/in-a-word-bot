from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, validators


class ResourceEditForm(FlaskForm):
    Url = StringField("Url: ", [
        validators.DataRequired("Url cannot be empty!")
    ], render_kw={"placeholder": "Url",
                  "class": "form-control",
                  "id": "inputUrl"})

    Description = StringField("Description: ", [
        validators.DataRequired("Description cannot be empty!")
    ], render_kw={"placeholder": "Description",
                  "class": "form-control",
                  "id": "inputDescription"})

    Submit = SubmitField("Change")
