from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class MyTextForm(FlaskForm):
    file = FileField(label='Выберите файл с текстом', validators=[DataRequired()])
    submit_btn = SubmitField(label='Загрузить', validators=[DataRequired()])
