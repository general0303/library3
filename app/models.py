from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    image = db.Column(db.String)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


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
    image = db.Column(db.String)

    def __repr__(self):
        return '<Author {}>'.format(self.name)

    def set_image(self, image):
        self.image = image

    def show_image(self):
        return self.image


class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(60), index=True)
    authors=db.relationship('Author', secondary=author_books, backref='books')
    image = db.Column(db.String)
    text = db.Column(db.String)

    def __repr__(self):
        return '<Book {}>'.format(self.name)

    def set_image(self, image):
        self.image = image

    def set_text(self, text):
        self.text = text

    def show_image(self):
        return self.image


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
