from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.category import Category

category_bp = Blueprint('category_bp', __name__, template_folder='../templates/categories')

@category_bp.route('/')
def category_list():
    categories = Category.query.all()
    return render_template('category_list.html', categories=categories)

@category_bp.route('/add', methods=['POST'])
def add_category():
    name = request.form['name']
    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()

    flash('Category added successfully', 'success')
    return redirect(url_for('category_bp.category_list'))
