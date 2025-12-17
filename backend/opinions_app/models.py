from datetime import datetime

from werkzeug.security import generate_password_hash,  check_password_hash

from flask_login import UserMixin

from . import db, login_manager

class Opinion(db.Model):
    __tablename__ = 'opinions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.String(1024), nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    added_by = db.Column(db.String(64))
    image_path = db.Column(db.String(256))
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    rating = db.Column(db.Integer, db.CheckConstraint('rating BETWEEN 0 AND 5'), nullable=True, default=0)
    reviews = db.relationship('Review', backref='parent_opinion', lazy='dynamic')

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id) 

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(508), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)
    opinions = db.relationship('Opinion', backref='users', lazy='dynamic')
    reviews = db.relationship('Review', backref='users', lazy='dynamic')


    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer(), primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    text = db.Column(db.String, nullable=True)
    opinion = db.Column(db.Integer, db.ForeignKey('opinions.id', ondelete='CASCADE'), nullable=True)
    rating = db.Column(db.Integer, db.CheckConstraint('rating BETWEEN 0 AND 5'), nullable=True)
    pub_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint(author, opinion, name='unique_author_opinion'),
    )