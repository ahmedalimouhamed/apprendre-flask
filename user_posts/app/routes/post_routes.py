import os
import time

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.post import Post
from app.models.user import User
from app.models.category import Category
from werkzeug.utils import secure_filename


post_bp = Blueprint('post_bp', __name__, template_folder='../templates/posts')

@post_bp.route('/')
def post_list():
    posts = Post.query.all()
    return render_template('post_list.html', posts=posts)

@post_bp.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = request.form['user_id']
        category_ids = request.form.getlist('categories')
        cover_image = request.files['cover_image']

        if cover_image:

            filename = secure_filename(f"{int(time.time())}_{cover_image.filename}")

            # Ensure filename is safe and save the file
            upload_folder = os.path.join('app', 'static', 'uploads', 'post_images')
            os.makedirs(upload_folder, exist_ok=True)  # Ensure the directory exists
            image_path = os.path.join(upload_folder, filename)
            cover_image.save(image_path)

            image_url = f'uploads/post_images/{filename}'

        else:
            image_url = None

        new_post = Post(title=title, content=content, cover_image=image_url, user_id=user_id)
        db.session.add(new_post)

        for category_id in category_ids:
            category = Category.query.get(category_id)
            new_post.categories.append(category)

        db.session.commit()

        flash('Post added successfully', 'success')
        return redirect(url_for('post_bp.post_list'))

    users = User.query.all()
    categories = Category.query.all()
    return render_template('add_post.html', users=users, categories=categories)