from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField("Correo electronico", validators=[DataRequired(), Email()])
    password = PasswordField("Contrasena", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesion")