import os

from uuid import uuid4
from werkzeug.utils import secure_filename


from random import randrange

from flask import abort, flash, redirect, render_template, url_for, send_from_directory, request, session, make_response, render_template_string
from flask_mail import Message
from flask_login import login_required

from . import app, db, mail
from .forms import OpinionForm, RegistrationForm, LoginForm
from .models import Opinion, User

@app.route('/')
def index_view():
    print('1', session.items())
    quantity = Opinion.query.count()
    if not quantity:
        abort(500)
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    return render_template('opinion.html', opinion=opinion)
    

@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        if Opinion.query.filter_by(text=text).first() is not None:
            flash('Такое мнение уже было оставлено ранее!')
            return render_template('add_opinion.html', form=form)
        # добавляем тут
        uploaded_image = form.image.data
        if uploaded_image:
            ext = os.path.splitext(uploaded_image.filename)[1].lower()
            filename = f'{uuid4().hex}{ext}'
            save_path = os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename)
            uploaded_image.save(save_path)
            image_path = f'/media/{filename}'
        else:
            image_path = None

        opinion = Opinion(
            title=form.title.data, 
            text=text, 
            source=form.source.data,
            image_path=image_path

        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)

@app.route('/opinions/<int:id>')
def opinion_view(id):
    opinion = Opinion.query.get_or_404(id)
    opinion.image_path = opinion.image_path.split('/')[2]
    return render_template('opinion.html', opinion=opinion) 

@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(app.config['UPLOADED_IMAGES_DEST'], filename)


@app.route('/mail')
def send_mail():
    msg = Message(
        subject="Тестовое письмо от Flask",
        sender=app.config['MAIL_USERNAME'],
        recipients=['andrejmartanov782@gmail.com']
    )
    mail.send(msg)
    return make_response('Good', 200)

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() or User.query.filter_by(email=form.email.data).first():
            flash('такой пользователь уже существует!')
            return render_template('registration.html', form=form)
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.password_hash = user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)
