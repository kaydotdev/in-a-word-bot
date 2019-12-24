from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField


class GenerateLectureForm(FlaskForm):
    Header = StringField("Header for a new lecture", [
        validators.DataRequired("Lecture header cannot be empty!")
    ], render_kw={"placeholder": "Header for a new lecture"})

    Submit = SubmitField("Generate")
