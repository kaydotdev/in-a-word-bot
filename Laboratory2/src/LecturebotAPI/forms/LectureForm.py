from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class LectureForm(FlaskForm):
    Owner = StringField("Owner login: ", [
        validators.DataRequired("Owner login cannot be empty!")
    ], render_kw={"placeholder": "Owner: "})

    Header = StringField("Lecture header: ", [
        validators.DataRequired("Lecture header cannot be empty!")
    ], render_kw={"placeholder": "Header: "})

    Content = StringField("Lecture content: ", [
        validators.DataRequired("Lecture content cannot be empty!")
    ], render_kw={"placeholder": "Content: "})

    Submit = SubmitField("Add")
