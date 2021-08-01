from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, URL, ValidationError


class NewResourceForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = TextAreaField("Описание")
    intensity = IntegerField('Трудоемкость')
    dim = StringField('единица измерения')
    duration = IntegerField('Длительность изучения (в неделях)')
    completed = IntegerField('Выполнено')
    progress = IntegerField('Прогресс')
    submit = SubmitField('Добавить')


class CheckProgressForm(FlaskForm):
    completed = IntegerField('Выполнено')

    submit = SubmitField('Изменить')

