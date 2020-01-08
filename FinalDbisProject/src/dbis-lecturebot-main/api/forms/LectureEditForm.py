from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, validators, TextAreaField


class LectureEditForm(FlaskForm):
    id = HiddenField("Id")

    Header = StringField("Lecture header: ", [
        validators.DataRequired("Lecture header cannot be empty!")
    ], render_kw={"placeholder": "Header",
                  "class": "form-control",
                  "id": "inputHeader"})

    Content = TextAreaField("Lecture content: ", [
        validators.DataRequired("Lecture content cannot be empty!")
    ], render_kw={"placeholder": "Content",
                  "class": "form-control",
                  "id": "inputContent"})

    Submit = SubmitField("Change")
