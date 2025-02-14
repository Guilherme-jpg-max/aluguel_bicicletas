from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
import os

db = SQLAlchemy()

def create_app(config_name=None):
    app = Flask(__name__)

    # Se 'config_name' não for fornecido, use o valor da variável de ambiente FLASK_ENV
    if not config_name:
        config_name = os.getenv('FLASK_ENV', 'development')  # Padrão para 'development'

    # Carregar a configuração com base no 'config_name'
    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    with app.app_context():
        # Importação das rotas
        from .routes.admin import admin_bp
        from .routes.usuario import user_bp
        from .routes.main import main_bp

        # Registrando os blueprints
        app.register_blueprint(admin_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(main_bp)

        db.create_all()  # Cria as tabelas no banco de dados

    return app
