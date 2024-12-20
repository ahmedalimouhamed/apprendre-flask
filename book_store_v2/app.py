from flask import Flask
from models import db
from controllers.author_controller import author_blueprint
from controllers.book_controller import book_blueprint

app = Flask(__name__)

app.config.from_object('config.Config')

db.init_app(app)

app.register_blueprint(author_blueprint, url_prefix='/authors')
app.register_blueprint(book_blueprint, url_prefix='/books')

with app.app_context():
    try:
        db.create_all()
        print('Database connected and tables created')
    except Exception as e:
        print(f"Error connecting to the database : {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)