from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')