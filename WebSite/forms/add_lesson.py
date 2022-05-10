from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddingLessonForm(FlaskForm):
    text_field = StringField('Текст для добавления', validators=[DataRequired()])
    submit_button = SubmitField('Добавить')
