from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField


class LectureForm(FlaskForm):
    Header = StringField("Lecture header: ", [
        validators.DataRequired("Lecture header cannot be empty!")
    ], render_kw={"placeholder": "Header: "})

    Content = TextAreaField("Lecture content: ", [
        validators.DataRequired("Lecture content cannot be empty!")
    ], render_kw={"placeholder": "Content: "})

    Submit = SubmitField("Add")
