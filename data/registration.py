from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, IntegerField, BooleanField, StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired


class Registration(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    hashed_password = PasswordField('Пароль', validators=[DataRequired()])
    modified_date = DateField('дата изменения', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')