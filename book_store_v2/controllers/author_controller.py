from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.author import Author

author_blueprint = Blueprint('author_blueprint', __name__)

@author_blueprint.route('/')
def list_authors():
    authors = Author.query.all()
    print(authors)
    return render_template('authors.html', authors=authors)

@author_blueprint.route('/add', methods=['POST'])
def add_author():
    try:
        name = request.form['name']
        bio = request.form['bio']
        new_author = Author(name = name, bio = bio)
        db.session.add(new_author)
        db.session.commit()
        flash('Author added successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding author : {str(e)}', 'danger')
    return redirect(url_for('author_blueprint.list_authors'))


@author_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_author(id):
    author = Author.query.get_or_404(id)
    if request.method == 'POST':
        try:
            author.name = request.form['name']
            author.bio = request.form['bio']
            db.session.commit()
            flash('Author updated successfully', 'success')
            return redirect(url_for('author_blueprint.list_authors'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating author : {str(e)}', 'danger')
    return render_template('edit_author.html', author=author)


@author_blueprint.route('/delete/<int:id>', methods=['POST'])
def delete_author(id):
    author = Author.query.get_or_404(id)
    try:
        db.session.delete(author)
        db.session.commit()
        flash('Author deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting author: {str(e)}', 'danger')
    return redirect(url_for('author_blueprint.list_authors'))