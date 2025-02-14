import pytest
from app import db
from app.models import Administrador, Estacao, Bicicleta

def test_cadastrar_admin(client):
    response = client.post('/admin/cadastrar', data={
        'nome': 'Novo Admin',
        'email': 'novo@admin.com',
        'senha': 'senha123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Administrador cadastrado com sucesso!' in response.data

def test_login_admin(client, init_database):
    response = client.post('/admin/login', data={
        'email': 'admin@test.com',
        'senha': 'senha123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login realizado com sucesso!' in response.data

def test_admin_dashboard(client, init_database):
    # Primeiro, faça login
    client.post('/admin/login', data={
        'email': 'admin@test.com',
        'senha': 'senha123'
    }, follow_redirects=True)

    response = client.get('/admin/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data

def test_adicionar_estacao(client, init_database):
    # Primeiro, faça login
    client.post('/admin/login', data={
        'email': 'admin@test.com',
        'senha': 'senha123'
    }, follow_redirects=True)

    response = client.post('/admin/estacoes/adicionar', data={
        'nome': 'Nova Estacao',
        'localizacao': 'Novo Local',
        'capacidade': 20
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Estação adicionada com sucesso!' in response.data.decode('utf-8')

def test_adicionar_bicicleta(client, init_database):
    # Primeiro, faça login
    client.post('/admin/login', data={
        'email': 'admin@test.com',
        'senha': 'senha123'
    }, follow_redirects=True)

    response = client.post('/admin/bicicletas/adicionar', data={
        'modelo': 'Novo Modelo',
        'numero_serie': '67890',
        'estacao_id': 1
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Bicicleta adicionada com sucesso!' in response.data

def test_remover_estacao(client, init_database):
    # Primeiro, faça login
    client.post('/admin/login', data={
        'email': 'admin@test.com',
        'senha': 'senha123'
    }, follow_redirects=True)

    response = client.post('/admin/estacoes/remover/1', follow_redirects=True)
    assert response.status_code == 200
    assert 'Estação e bicicletas associadas removidas com sucesso!' in response.data.decode('utf-8')

def test_remover_bicicleta(client, init_database):
    # Primeiro, faça login
    client.post('/admin/login', data={
        'email': 'admin@test.com',
        'senha': 'senha123'
    }, follow_redirects=True)

    response = client.post('/admin/bicicletas/remover/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'Bicicleta removida com sucesso!' in response.data