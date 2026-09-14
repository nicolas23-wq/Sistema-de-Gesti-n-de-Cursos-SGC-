from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class CalificacionForm(FlaskForm):
    curso_id = SelectField("Curso", coerce=int, validators=[DataRequired()])
    estudiante_id = SelectField("Estudiante", coerce=int, validators=[DataRequired()])
    nota = FloatField("Nota (0 - 20)", validators=[DataRequired(), NumberRange(min=0, max=20)])
    submit = SubmitField("Guardar calificacion")