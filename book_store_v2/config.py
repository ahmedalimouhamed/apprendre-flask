class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/bookstore_db_flask_v2"
    SQL_ALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = "secret"