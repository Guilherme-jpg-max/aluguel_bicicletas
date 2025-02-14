import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sua_chave_secreta_aqui')  # Usar uma variável de ambiente para segurança
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI', 'sqlite:///dev.db')

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI', 'sqlite:///test.db')
    TESTING = True  # Ativa o modo de teste do Flask

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI', 'postgresql://user:pass@localhost/prod')
