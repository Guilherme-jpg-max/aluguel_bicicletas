import pytest
from app import create_app, db
from app.models import Administrador, Usuario, Estacao, Bicicleta, Aluguel

@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing') 
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

# Testando o modelo Administrador
def test_administrador_criar(test_client):
    administrador = Administrador(nome='Admin Test', email='admin@test.com', senha_hash='senha')
    administrador.set_senha('12345')
    db.session.add(administrador)
    db.session.commit()
    
    assert administrador.nome == 'Admin Test'
    assert administrador.email == 'admin@test.com'
    assert administrador.check_senha('12345')


def test_usuario_criar(test_client):
    usuario = Usuario(nome='Usuario Test', email='usuario@test.com', saldo=50.0)
    usuario.set_senha('senha123')
    db.session.add(usuario)
    db.session.commit()

    # Verificar se o usuário foi criado corretamente
    assert usuario.nome == 'Usuario Test'
    assert usuario.email == 'usuario@test.com'
    assert usuario.saldo == 50.0
    assert usuario.check_senha('senha123')

# Testando o modelo Estacao
def test_estacao_criar(test_client):
    administrador = Administrador.query.first()
    estacao = Estacao(nome='Estação Central', localizacao='Centro', capacidade=20, administrador_id=administrador.id)
    db.session.add(estacao)
    db.session.commit()

    # Verificar se a estação foi criada corretamente
    assert estacao.nome == 'Estação Central'
    assert estacao.localizacao == 'Centro'
    assert estacao.capacidade == 20

# Testando o modelo Bicicleta
def test_bicicleta_criar(test_client):
    administrador = Administrador.query.first()
    estacao = Estacao.query.first()
    bicicleta = Bicicleta(modelo='Bicicleta Test', numero_serie='123456', valor_por_hora=10.0, administrador_id=administrador.id, estacao_id=estacao.id)
    db.session.add(bicicleta)
    db.session.commit()

    # Verificar se a bicicleta foi criada corretamente
    assert bicicleta.modelo == 'Bicicleta Test'
    assert bicicleta.numero_serie == '123456'
    assert bicicleta.valor_por_hora == 10.0
    assert bicicleta.estacao_id == estacao.id

# Testando o modelo Aluguel
def test_aluguel_criar(test_client):
    usuario = Usuario.query.first()
    bicicleta = Bicicleta.query.first()
    aluguel = Aluguel(usuario_id=usuario.id, bicicleta_id=bicicleta.id, administrador_id=bicicleta.administrador_id)
    db.session.add(aluguel)
    db.session.commit()

    # Verificar se o aluguel foi criado corretamente
    assert aluguel.usuario_id == usuario.id
    assert aluguel.bicicleta_id == bicicleta.id
    assert aluguel.data_inicio is not None

