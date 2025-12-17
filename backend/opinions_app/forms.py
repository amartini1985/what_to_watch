from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField, FileField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, ValidationError, Email
from .models import Review

# class UniqueFieldValidator:
#     def __init__(self, model, first_field, second_field):
#         self.model = model
#         self.first_field = first_field
#         self.second_field = second_field

#     def __call__(self, form, field):
#         obj = self.model.query.filter_by(
#             **{
#                 self.first_field: form[self.first_field].data,
#                 self.second_field: form[self.second_field].data,
#             }
#         ).first()
#         if obj:
#             raise ValidationError('Така запись уже есть')    



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
    image = FileField('Изображение')
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
                    Email(message='Формат почты должен соответствовать требованиям'),
                    Length(1, 128), ]
    )
    password = PasswordField(
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
    password = PasswordField(
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
    oldpassword = PasswordField(
        'Введите ваш старый password', 
        validators=[DataRequired(message='Обязательное поле'), 
                    Length(1, 128)]
    )
    newpassword = PasswordField(
        'Введите ваш новый password', 
        validators=[DataRequired(message='Обязательное поле'), 
                    Length(1, 128)]
    )
    submit = SubmitField('Сменить пароль')


class EmailForRecoverPasswordForm(FlaskForm):
    '''Форма ввода email для восстановления пароля.'''
    email = StringField(
        'Напишите ваш email', 
        validators=[DataRequired(message='Обязательное поле'), 
                    Length(1, 128)]
    )
    submit = SubmitField('Отправить код')


class RecoverPasswordForm(FlaskForm):
    '''Форма ввода email для восстановления пароля.'''
    confirmation_code = StringField(
        'Введите ваш confirmation_code', 
        validators=[DataRequired(message='Обязательное поле'), 
                    Length(1, 128)]
    )
    newpassword = PasswordField(
        'Введите ваш новый password', 
        validators=[DataRequired(message='Обязательное поле'), 
                    Length(1, 128)]
    )
    submit = SubmitField('Отправить код')

class ReviewForm(FlaskForm):
    text = TextAreaField(
        'Напишите мнение', 
        validators=[DataRequired(message='Обязательное поле')]
    )
    rating = IntegerField(
        'Введите оценку произведения',
        validators=[DataRequired(message='Обязательное поле'),
                    NumberRange(min=0, max=5, message='Оценка должна быть от 0 до 5')
                    ]
    )
    submit = SubmitField('Добавить')