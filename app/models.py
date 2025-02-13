from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Administrador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)

    # Relacionamentos
    estacoes = db.relationship('Estacao', backref='administrador', lazy=True)  
    bicicletas = db.relationship('Bicicleta', backref='administrador', lazy=True)
    alugueis = db.relationship('Aluguel', back_populates='administrador')

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)

    alugueis = db.relationship('Aluguel', back_populates='usuario')

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


class Estacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    localizacao = db.Column(db.String(255), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    administrador_id = db.Column(db.Integer, db.ForeignKey('administrador.id'), nullable=False)  
    bicicletas = db.relationship('Bicicleta', back_populates='estacao')  


class Bicicleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    numero_serie = db.Column(db.String(50), nullable=False)  
    status = db.Column(db.String(20), default='disponivel')
    estacao_id = db.Column(db.Integer, db.ForeignKey('estacao.id'), nullable=True)
    administrador_id = db.Column(db.Integer, db.ForeignKey('administrador.id'), nullable=False)

    estacao = db.relationship('Estacao', back_populates='bicicletas')
    alugueis = db.relationship('Aluguel', back_populates='bicicleta')


class Aluguel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    bicicleta_id = db.Column(db.Integer, db.ForeignKey('bicicleta.id'), nullable=False)
    administrador_id = db.Column(db.Integer, db.ForeignKey('administrador.id'), nullable=False)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime, nullable=True)
    valor_total = db.Column(db.Float, nullable=True)

    usuario = db.relationship('Usuario', back_populates='alugueis')
    bicicleta = db.relationship('Bicicleta', back_populates='alugueis')
    administrador = db.relationship('Administrador', back_populates='alugueis')
