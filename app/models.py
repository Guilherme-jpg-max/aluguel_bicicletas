from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Administrador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    estacoes = db.relationship('Estacao', backref='administrador', lazy=True)  # Relacionamento com Estacao
    bicicletas = db.relationship('Bicicleta', backref='administrador', lazy=True)  # Relacionamento com Bicicleta

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Estacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    localizacao = db.Column(db.String(255), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    administrador_id = db.Column(db.Integer, db.ForeignKey('administrador.id'), nullable=False)  # Chave estrangeira para Administrador
    bicicletas = db.relationship('Bicicleta', back_populates='estacao')  # Relacionamento com Bicicleta


class Bicicleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    numero_serie = db.Column(db.String(50), nullable=False)  # Removido unique=True
    status = db.Column(db.String(20), default='disponivel')
    estacao_id = db.Column(db.Integer, db.ForeignKey('estacao.id'), nullable=True)
    administrador_id = db.Column(db.Integer, db.ForeignKey('administrador.id'), nullable=False)
    estacao = db.relationship('Estacao', back_populates='bicicletas')