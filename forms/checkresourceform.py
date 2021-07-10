from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired


class CheckProgressForm(FlaskForm):
    progress = IntegerField('Прогресс (в процентах)', validators=[DataRequired()])

    submit = SubmitField('Изменить')
