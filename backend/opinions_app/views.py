"""Представления для проекта what_to_watch."""

import os
import jwt

import datetime

from random import randrange
from uuid import uuid4
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import func

from flask import (
    abort, flash, redirect, render_template, url_for,
    send_from_directory, make_response, request
)
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message

from . import app, db, mail
from .forms import (
    OpinionForm,
    RegistrationForm,
    LoginForm,
    ChangePasswordForm,
    EmailForRecoverPasswordForm,
    RecoverPasswordForm,
    ReviewForm
)
from .models import Opinion, User, Review
from .utils import get_rating_from_db

@app.route('/')
def index_view():
    """Представление для главной страницы."""
    quantity = Opinion.query.count()
    if not quantity:
        abort(500)
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    # rating = db.session.query(func.avg(Review.rating)).filter(Review.opinion == opinion.id).scalar()
    rating = get_rating_from_db(opinion.id)[0] # альтернативный способ
    opinion.rating = int(rating) if rating else 0
    return render_template('main/opinion.html', opinion=opinion)


@app.route('/all')
def opinions_view():
    """Представление для страницы всех произведений."""
    quantity = Opinion.query.count()
    if not quantity:
        abort(500)
    opinions = Opinion.query.all()
    for opinion in opinions:
        rating = db.session.query(func.avg(Review.rating)).filter(Review.opinion == opinion.id).scalar()
        opinion.rating = int(rating) if rating else 0
    return render_template('main/opinions.html', opinions=opinions)

@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    """Представление для добавление фильмов."""
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        if Opinion.query.filter_by(text=text).first() is not None:
            flash('Такое мнение уже было оставлено ранее!')
            return render_template('main/add_opinion.html', form=form)
        if current_user.is_anonymous:
            flash('Необходимо зарегистрироваться!')
            return render_template('main/add_opinion.html', form=form)            
        uploaded_image = form.image.data
        if uploaded_image:
            ext = os.path.splitext(uploaded_image.filename)[1].lower()
            filename = f'{uuid4().hex}{ext}'
            save_path = os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename)
            uploaded_image.save(save_path)
            image_path = f'{filename}'
        else:
            image_path = None
        opinion = Opinion(
            title=form.title.data,
            text=text,
            source=form.source.data,
            image_path=image_path,
            user=current_user.id
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('main/add_opinion.html', form=form)

@app.route('/opinions/<int:id>', methods=['GET', 'POST'])
def opinion_view(id):
    opinion = Opinion.query.get_or_404(id)
    form = ReviewForm()
    if form.validate_on_submit():
        if current_user.is_anonymous:
            flash('Необходимо зарегистрироваться!')
            return render_template('main/opinion_one.html', opinion=opinion, form=form)
        if Review.query.filter_by(author=current_user.id, opinion=id).first():
            flash('Добавить отзыв повторно нельзя!')
            return render_template('main/opinion_one.html', opinion=opinion, form=form)
        review = Review(
            author=current_user.id,
            text=form.text.data,
            opinion=id,
            rating=form.rating.data
        )
        db.session.add(review)
        db.session.commit()
    rating = db.session.query(func.avg(Review.rating)).filter(Review.opinion == id).scalar()
    return render_template('main/opinion_one.html', opinion=opinion, form=form, rating=rating) 

@app.route('/opinions/<int:id>/edit', methods=['GET', 'POST'])
def opinion_view_edit(id):
    opinion = Opinion.query.get_or_404(id)
    form = OpinionForm()
    value_text = form.text.data
    form.text.data = opinion.text
    form.title.data = opinion.title
    if form.validate_on_submit():
        opinion.text = value_text
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('opinion_one.html', opinion=opinion, form=form)

@app.route('/opinions/<int:id>/delete', methods=['GET', 'POST'])
def opinion_view_delete(id):
    opinion = Opinion.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(opinion)
        db.session.commit()
        return redirect(url_for('index_view'))
    return render_template('opinion_one.html', opinion=opinion)

@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(app.config['UPLOADED_IMAGES_DEST'], filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if not user:
            flash('Такого пользователя не существует!')
            return render_template('registration/login.html', form=form)
        if not user.check_password(form.password.data):
            flash('Пароль неверный!')
            return render_template('registration/login.html', form=form)                      
        login_user(user)
        return redirect(url_for('index_view'))
    return render_template('registration/login.html', form=form)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() or User.query.filter_by(email=form.email.data).first():
            flash('Такой пользователь уже существует!')
            return render_template('registration/registration.html', form=form)
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.password_hash = user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration/registration.html', form=form)

@app.route('/change_password', methods=['GET', 'POST', 'PATCH'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if not user:
            flash('Такой пользователь не существует!')
            return render_template('registration/change_password.html', form=form)
        if check_password_hash(user.password_hash, form.oldpassword.data):
            flash('вы ввели неверный пароль!')
            return render_template('registration/change_password.html', form=form)            
        user.password_hash = generate_password_hash(form.newpassword.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration/change_password.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))


@app.route('/mail')
def send_mail(email, confirmation_code):
    msg = Message(
        subject="Тестовое письмо от Flask",
        sender=app.config['MAIL_USERNAME'],
        recipients=['andrejmartanov782@gmail.com', str(email)],
        body=confirmation_code
    )
    mail.send(msg)
    return make_response('Good', 200)

def generate_reset_password_token(user_id):
    payload = {
        'sub': str(user_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return token

@app.route('/email_for_recover_password', methods=['GET', 'POST'])
def email_for_recover_password():
    form = EmailForRecoverPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Пользователь с таким email не зарегистрирован.')
            return render_template('email_for_recover_password.html', form=form)
        confirmation_code = generate_reset_password_token(user.id)
        send_mail(user.email, confirmation_code)
        logout_user()
        return redirect(url_for('recover_password'))
    return render_template('registration/email_for_recover_password.html', form=form)

@app.route('/recover_password', methods=['GET', 'POST'])
def recover_password():
    form = RecoverPasswordForm()
    if form.validate_on_submit():
        try:
            data_confirmation_code = jwt.decode(form.confirmation_code.data, os.getenv('SECRET_KEY'), algorithms='HS256')
            user_id = data_confirmation_code['sub']
            user = User.query.filter_by(id=user_id).first()
            if not user:
                flash('Неверные данные')
                return render_template('registration/recover_password.html', form=form)
            user.password_hash = generate_password_hash(form.newpassword.data)
            db.session.commit()
            return redirect(url_for('login'))
        except jwt.ExpiredSignatureError:
            flash('Время действия token истекло')
            return render_template('registration/recover_password.html', form=form)
        except jwt.InvalidTokenError:
            flash('Некорректный токен')
            return render_template('registration/recover_password.html', form=form)
    return render_template('registration/recover_password.html', form=form)

@app.route('/video')
def video():
    'Предствление для тестового видео'
    return render_template('video.html')

        # print('#' * 20, current_user.username)
        # print('#' * 20, current_user.email)
        # print('#' * 20, current_user.is_authenticated)   
        # print('#' * 20, current_user.is_active)
        # print('#' * 20, current_user.is_anonymous)   
        # print('#' * 20, current_user.get_id())