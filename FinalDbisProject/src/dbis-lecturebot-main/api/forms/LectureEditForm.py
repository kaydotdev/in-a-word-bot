from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, validators, TextAreaField


class LectureEditForm(FlaskForm):
    Content = TextAreaField("Lecture content: ", [
        validators.DataRequired("Lecture content cannot be empty!")
    ], render_kw={"placeholder": "Content",
                  "class": "form-control",
                  "id": "inputContent"})

    Submit = SubmitField("Change")
