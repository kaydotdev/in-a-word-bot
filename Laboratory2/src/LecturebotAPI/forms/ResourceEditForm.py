from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, validators


class ResourceEditForm(FlaskForm):
    id = HiddenField("Id")

    Description = StringField("Description: ", [
        validators.DataRequired("Description cannot be empty!")
    ], render_kw={"placeholder": "Description",
                  "class": "form-control",
                  "id": "inputDescription"})

    Submit = SubmitField("Change")
