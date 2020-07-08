from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


author_books=db.Table('author_books',
                      db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
                      db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)


class Author(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(60), index=True)

    def __repr__(self):
        return '<Author {}>'.format(self.name)


class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(60), index=True)
    authors=db.relationship('Author', secondary=author_books, backref='books')

    def __repr__(self):
        return '<Book {}>'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))