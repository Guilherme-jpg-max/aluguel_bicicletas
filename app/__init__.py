from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        # Importa e registra os Blueprints
        from .routes.admin import admin_bp
        from .routes.usuario import usuario_bp

        app.register_blueprint(admin_bp)
        app.register_blueprint(usuario_bp)

        db.create_all()  # Cria as tabelas no banco de dados

    return app