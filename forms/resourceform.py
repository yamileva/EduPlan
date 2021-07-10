from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired


class NewResourceForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = TextAreaField("Описание, ссылка")
    duration = IntegerField('Длительность изучения (в неделях)')
    progress = IntegerField('Прогресс (в процентах)')

    submit = SubmitField('Добавить')
