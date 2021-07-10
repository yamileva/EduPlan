from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class NewSectionForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    type = SelectField('Тип элемента', choices=[(0, "Раздел"), (1, "Точка контроля")], coerce=int)
    duration = IntegerField('Длительность изучения (в неделях)')
    submit = SubmitField('Добавить')
