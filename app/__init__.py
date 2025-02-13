from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from .routes.admin import admin_bp
        from .routes.usuario import user_bp
        from .routes.main import main_bp

        app.register_blueprint(admin_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(main_bp)

        db.create_all()  # Cria as tabelas no banco de dados

    return app
