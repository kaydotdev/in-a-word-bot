from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class LectureForm(FlaskForm):
    Owner = StringField("Owner login: ", [
        validators.DataRequired("Owner login cannot be empty!")
    ])

    Header = StringField("Lecture header: ", [
        validators.DataRequired("Lecture header cannot be empty!")
    ])

    Content = StringField("Lecture content: ", [
        validators.DataRequired("Lecture content cannot be empty!")
    ])

    submit = SubmitField("Add")
