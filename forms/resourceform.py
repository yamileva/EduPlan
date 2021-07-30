from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, URL, ValidationError


class NewResourceForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = TextAreaField("Описание")
    intensity = StringField('Трудоемкость')
    duration = IntegerField('Длительность изучения (в неделях)')
    progress = IntegerField('Прогресс')
    submit = SubmitField('Добавить')

