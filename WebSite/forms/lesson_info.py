from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField
from wtforms.validators import DataRequired


class LessonInfoForm(FlaskForm):
    time = IntegerField(validators=[DataRequired()])
    average_speed = FloatField(validators=[DataRequired()])
