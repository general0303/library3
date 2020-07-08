from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User, Author, Book
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from app.forms import AddAuthorForm, AddBookForm, DeleteAuthorForm, DeleteBookForm, EditAuthorForm, EditBookForm, SearchBooksForm


@app.route('/')
@app.route('/index')
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title='Home Page', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/show_authors')
def show_authors():
    return render_template('show_authors.html', title='Authors', authors=Author.query.all())


@app.route('/show_books')
def show_books():
    return render_template('show_books.html', title='Books', books=Book.query.all())


@app.route('/add_author', methods=['GET', 'POST'])
@login_required
def add_author():
    form = AddAuthorForm()
    if form.validate_on_submit():
        books = []
        title1 = form.title1.data
        title2 = form.title2.data
        title3 = form.title3.data
        title4 = form.title4.data
        title5 = form.title5.data
        bs=Book.query.all()
        for book in bs:
            if book.name == title1:
                books.append(book)
            if book.name == title2:
                books.append(book)
            if book.name == title3:
                books.append(book)
            if book.name == title4:
                books.append(book)
            if book.name == title5:
                books.append(book)
        author = Author(name=form.name.data, books=books)
        db.session.add(author)
        db.session.commit()
        flash('Congratulations, you added a new author!')
        return redirect(url_for('show_authors'))
    return render_template('add_author.html', title='Add author', form=form)


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        book = Book(name=form.name.data)
        db.session.add(book)
        db.session.commit()
        flash('Congratulations, you added a new book!')
        return redirect(url_for('show_books'))
    return render_template('add_book.html', title='Add book', form=form)


@app.route('/delete_author', methods=['GET', 'POST'])
@login_required
def delete_author():
    form = DeleteAuthorForm()
    name = form.name.data
    if form.validate_on_submit():
        author = Author.query.filter_by(name = name).first()
        db.session.delete(author)
        db.session.commit()
        flash('Congratulations, you deleted a author!')
        return redirect(url_for('show_authors'))
    return render_template('delete_author.html', title='Delete author', form=form)


@app.route('/delete_book', methods=['GET', 'POST'])
@login_required
def delete_book():
    form = DeleteBookForm()
    name = form.name.data
    if form.validate_on_submit():
        book = Book.query.filter_by(name = name).first()
        db.session.delete(book)
        db.session.commit()
        flash('Congratulations, you deleted a book!')
        return redirect(url_for('show_books'))
    return render_template('delete_book.html', title='Delete book', form=form)


@app.route('/edit_author', methods=['GET', 'POST'])
@login_required
def edit_author():
    form = EditAuthorForm()
    if form.validate_on_submit():
        title = form.title.data
        name = form.name.data
        new_name = form.new_name.data
        a = Author.query.filter_by(name = name).first()
        books = a.books
        b = Book.query.filter_by(name = title).first()
        books.append(b)
        a.name=new_name
        a.books=books
        db.session.commit()
        flash('Congratulations, you edited a new author!')
        return redirect(url_for('show_authors'))
    return render_template('edit_author.html', title='Edit author', form=form)


@app.route('/edit_book', methods=['GET', 'POST'])
@login_required
def edit_book():
    form = EditBookForm()
    if form.validate_on_submit():
        name = form.name.data
        new_name = form.new_name.data
        b = Book.query.filter_by(name = name).first()
        b.name=new_name
        db.session.commit()
        flash('Congratulations, you edited a new book!')
        return redirect(url_for('show_books'))
    return render_template('edit_book.html', title='Edit book', form=form)


@app.route('/search_books', methods=['GET', 'POST'])
def search_books():
    form = SearchBooksForm()
    if form.validate_on_submit():
        name = form.name.data
        a = Author.query.filter_by(name = name).first()
        books=a.books
        return render_template('show_books.html', title='Books', books=books)
    return render_template('search_book.html', title='Search book', form=form)