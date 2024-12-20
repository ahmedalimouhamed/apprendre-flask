from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.book import Book
from models.author import Author

book_blueprint = Blueprint('book_blueprint', __name__)

@book_blueprint.route('/')
def list_books():
    books = Book.query.all()
    authors = Author.query.all()
    return render_template('books.html', books=books, authors=authors)

@book_blueprint.route('/add', methods=['POST'])
def add_book():
    try:
        title = request.form['title']
        genre = request.form['genre']
        author_id = request.form['author_id']
        new_book = Book(title=title, genre=genre, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding book : {str(e)}', 'danger')
    return redirect(url_for('book_blueprint.list_books'))

@book_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    authors = Author.query.all()
    if request.method == 'POST':
        try:
            book.title = request.form['title']
            book.genre = request.form['genre']
            book.author_id = request.form['author_id']
            db.session.commit()
            flash('Book updated successfully!', 'success')
            return redirect(url_for('book_blueprint.list_books'))
        except Exception as e:
            db.session.roolback()
            flash(f'Error updating book: {str(e)}', 'danger')
    return render_template('edit_book.html', book=book, authors=authors)

@book_blueprint.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    try:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully', 'success')
    except Exception as e:
        db.session(f'Error deleting book {str(e)}', 'danger')
    return redirect(url_for('book_blueprint.list_books'))