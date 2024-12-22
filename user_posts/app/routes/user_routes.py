import time

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import db
from app.models.user import User
import os

user_bp = Blueprint('user_bp', __name__, template_folder='../templates/users')


@user_bp.route('/')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@user_bp.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        profile_image = request.files['profile_image']

        if profile_image:
            filename = secure_filename(f"{int(time.time())}_{profile_image.filename}")

            # Ensure filename is safe and save the file
            upload_folder = os.path.join('app', 'static', 'uploads', 'profile_pics')
            os.makedirs(upload_folder, exist_ok=True)  # Ensure the directory exists
            image_path = os.path.join(upload_folder, filename)
            profile_image.save(image_path)

            image_url = f'uploads/profile_pics/{filename}'

        else:
            image_url= None

        new_user = User(username=username, email=email, profile_image=image_url)
        db.session.add(new_user)
        db.session.commit()

        flash('User added successfully', 'success')
        return redirect(url_for('user_bp.user_list'))

    return render_template('add_user.html')