import pytest
from app import create_app, db
from app.models import Administrador, Estacao, Bicicleta, Aluguel

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        admin = Administrador(nome='Admin Test', email='admin@test.com')
        admin.set_senha('senha123')
        db.session.add(admin)
        db.session.commit()

        estacao = Estacao(nome='Estacao Test', localizacao='Local Test', capacidade=10, administrador_id=admin.id)
        db.session.add(estacao)
        db.session.commit()

        bicicleta = Bicicleta(modelo='Modelo Test', numero_serie='12345', estacao_id=estacao.id, administrador_id=admin.id)
        db.session.add(bicicleta)
        db.session.commit()

        yield db
