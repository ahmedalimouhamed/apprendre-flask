import os


class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/users_post_db_flask"
    SQLALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = "secret"

    UPLOADED_PROFILE_PICS_DEST = os.path.join('app', 'static', 'uploads', 'profile_pics')
    UPLOADED_POST_IMAGES_DEST = os.path.join('app', 'static', 'uploads', 'post_images')