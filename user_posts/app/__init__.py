from flask  import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')
    db.init_app(app)
    #migrate.init_app(app, db)

    from app.routes.user_routes import user_bp
    from app.routes.post_routes import post_bp
    from app.routes.category_routes import category_bp

    app.register_blueprint(user_bp, url_prefix = '/users')
    app.register_blueprint(post_bp, url_prefix = '/posts')
    app.register_blueprint(category_bp, url_prefix = '/categories')

    with app.app_context():
        try:
            db.create_all()
            print('Database connected and tables created')
        except Exception as e:
            print(f"Error connecting to the database : {str(e)}")

    return app