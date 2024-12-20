from flask import Flask, render_template, request, redirect, url_for
from forms import AuthorForm, BookForm
from sqlalchemy import text  # Import text to handle raw SQL queries
from models import db, Author, Book

app = Flask(__name__)

app.config.from_object('config.Config')

# Initialize the database with the app
db.init_app(app)

# Check the database connection on app startup
with app.app_context():
    try:
        # Perform a simple query to check the connection using text()
        db.session.execute(text('SELECT 1'))
        print("Database is connected successfully!")
        db.create_all()  # Optional: Create tables if not already created
    except Exception as e:
        print(f"Database connection failed: {str(e)}")


@app.route('/authors', methods=['GET', 'POST'])
def manage_authors():
    form = AuthorForm()
    if form.validate_on_submit():
        new_author = Author(name=form.name.data, bio=form.bio.data)
        db.session.add(new_author)
        db.session.commit()
        return redirect(url_for('manage_authors'))
    authors = Author.query.all()
    return render_template('authors.html', form=form, authors=authors)


@app.route('/authors/<int:author_id>', methods=['GET', 'POST'])
def edit_author(author_id):
    author = Author.query.get_or_404(author_id)
    form = AuthorForm(obj=author)

    if form.validate_on_submit():
        author.name = form.name.data
        author.bio = form.bio.data
        db.session.commit()
        return redirect(url_for('manage_authors'))

    return render_template('edit_author.html', form=form, author=author)

@app.route('/authors/delete/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    return redirect(url_for('manage_authors'))



@app.route('/books', methods=['GET', 'POST'])
def manage_books():
    form = BookForm()
    form.author.choices = [(author.id, author.name) for author in Author.query.all()]
    if form.validate_on_submit():
        print(form.data)
        new_book = Book(title=form.title.data, genre=form.genre.data, author_id=form.author.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('manage_books'))
    books = Book.query.all()
    return render_template('books.html', form=form, books=books)

@app.route('/books/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    form.author.choices = [(author.id, author.name) for author in Author.query.all()]

    if request.method == 'GET':
        form.title.data = book.title
        form.genre.data = book.genre
        form.author.data = book.author_id

    if form.validate_on_submit():
        book.title = form.title.data
        book.genre = form.genre.data
        book.author_id = form.author.data
        db.session.commit()
        return redirect(url_for('manage_books'))

    return render_template('edit_book.html', form=form, book=book)

@app.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('manage_books'))

if __name__ == '__main__':
    app.run(debug=True)
