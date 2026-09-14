from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class CrearCursoForm(FlaskForm):
    nombre = StringField("Nombre del curso", validators=[DataRequired(), Length(max=120)])
    descripcion = TextAreaField("Descripcion", validators=[Length(max=500)])
    docente_id = SelectField("Docente asignado", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Crear curso")


class InscribirEstudianteForm(FlaskForm):
    curso_id = SelectField("Curso", coerce=int, validators=[DataRequired()])
    estudiante_id = SelectField("Estudiante", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Inscribir estudiante")


class CrearUsuarioForm(FlaskForm):
    nombre = StringField("Nombre completo", validators=[DataRequired(), Length(max=100)])
    email = StringField("Correo electronico", validators=[DataRequired(), Email()])
    password = PasswordField("Contrasena", validators=[DataRequired(), Length(min=6)])
    rol = SelectField(
        "Rol",
        choices=[("docente", "Docente"), ("estudiante", "Estudiante")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Crear usuario")