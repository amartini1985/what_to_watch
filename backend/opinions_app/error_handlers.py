# what_to_watch/opinions_app.py

from flask import render_template

from . import app, db


@app.errorhandler(500)
def internal_error(error):
    # Ошибка 500 возникает в нештатных ситуациях на сервере. 
    # Например, провалилась валидация данных.
    # В таких случаях можно откатить изменения, незафиксированные в БД,
    # чтобы в базу не записалось ничего лишнего.
    db.session.rollback()
    # Пользователю вернётся страница, сгенерированная на основе 500.html.
    # Этого шаблона пока нет, но сейчас вы его тоже создадите.
    # Пользователь получит и код HTTP-ответа 500.
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404