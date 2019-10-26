from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, validators


class LectureEditForm(FlaskForm):
    id = HiddenField("Id")

    Owner = StringField("Owner login: ", [
        validators.DataRequired("Owner login cannot be empty!")
    ], render_kw={"placeholder": "Owner",
                  "class": "form-control",
                  "id": "inputOwner"})

    Header = StringField("Lecture header: ", [
        validators.DataRequired("Lecture header cannot be empty!")
    ], render_kw={"placeholder": "Header",
                  "class": "form-control",
                  "id": "inputHeader"})

    Content = StringField("Lecture content: ", [
        validators.DataRequired("Lecture content cannot be empty!")
    ], render_kw={"placeholder": "Content",
                  "class": "form-control",
                  "id": "inputContent"})

    Submit = SubmitField("Change")
