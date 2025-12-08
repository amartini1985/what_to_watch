from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField, FileField
from wtforms.validators import DataRequired, Length, Optional

class OpinionForm(FlaskForm):
    title = StringField(
        'Введите название фильма',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    text = TextAreaField(
        'Напишите мнение', 
        validators=[DataRequired(message='Обязательное поле')]
    )
    image = FileField('Изображение') # Сюда
    source = URLField(
        'Добавьте ссылку на подробный обзор фильма',
        validators=[Length(1, 256), Optional()]
    )
    submit = SubmitField('Добавить')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Введите ваш username',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    email = StringField(
        'Напишите ваш email', 
        validators=[DataRequired(message='Обязательное поле'), 
                    Length(1, 128)]
    )
    password = StringField(
        'Напишите ваш password', 
        validators=[DataRequired(message='Обязательное поле'), 
                    Length(1, 128)]
    )
    submit = SubmitField('Добавить')


class LoginForm(FlaskForm):
    username = StringField(
        'Введите ваш username',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    password = StringField(
        'Напишите ваш password', 
        validators=[DataRequired(message='Обязательное поле'), 
                    Length(1, 128)]
    )
    submit = SubmitField('Авторизоваться')


class ChangePasswordForm(FlaskForm):
    '''Форма для изменения паролей'''
    username = StringField(
        'Введите ваш username',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    oldpassword = StringField(
        'Введите ваш старый password', 
        validators=[DataRequired(message='Обязательное поле'), 
                    Length(1, 128)]
    )
    newpassword = StringField(
        'Введите ваш новый password', 
        validators=[DataRequired(message='Обязательное поле'), 
                    Length(1, 128)]
    )
    submit = SubmitField('Сменить пароль')