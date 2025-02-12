from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from app.models import Estacao, Bicicleta, Administrador
from app import db

# Cria um Blueprint para as rotas de administração
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorator para verificar se o administrador está logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'error')
            return redirect(url_for('admin.login'))
        
        # Verifica se o administrador ainda existe no banco de dados
        admin = Administrador.query.get(session['admin_id'])
        if not admin:
            session.pop('admin_id', None)  # Encerra a sessão
            flash('Sua conta foi removida. Por favor, faça login novamente.', 'error')
            return redirect(url_for('admin.login'))
        
        return f(*args, **kwargs)
    return decorated_function

# Rota para cadastrar um administrador
@admin_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_admin():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Verifica se o email já está cadastrado
        if Administrador.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'error')
            return redirect(url_for('admin.cadastrar_admin'))

        # Cria um novo administrador
        novo_admin = Administrador(nome=nome, email=email)
        novo_admin.set_senha(senha)  # Gera o hash da senha
        db.session.add(novo_admin)
        db.session.commit()

        flash('Administrador cadastrado com sucesso!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/cadastrar_admin.html')

# Rota para o dashboard do administrador (protegida)
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    administradores = Administrador.query.all()
    return render_template('admin/dashboard.html', administradores=administradores)

# Rota para listar estações (protegida)
@admin_bp.route('/estacoes')
@login_required
def admin_estacoes():
    # Obtém o ID do administrador logado
    admin_id = session.get('admin_id')
    
    # Filtra as estações pelo administrador logado
    estacoes = Estacao.query.filter_by(administrador_id=admin_id).all()
    
    return render_template('admin/estacoes.html', estacoes=estacoes)

# Rota para adicionar uma estação (protegida)
@admin_bp.route('/estacoes/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_estacao():
    if request.method == 'POST':
        nome = request.form['nome']
        localizacao = request.form['localizacao']
        capacidade = request.form['capacidade']
        admin_id = session.get('admin_id')  # Obtém o ID do administrador logado

        nova_estacao = Estacao(nome=nome, localizacao=localizacao, capacidade=capacidade, administrador_id=admin_id)
        db.session.add(nova_estacao)
        db.session.commit()

        flash('Estação adicionada com sucesso!', 'success')
        return redirect(url_for('admin.admin_estacoes'))

    return render_template('admin/adicionar_estacao.html')

# Rota para listar bicicletas (protegida)
@admin_bp.route('/bicicletas')
@login_required
def admin_bicicletas():
    # Obtém o ID do administrador logado
    admin_id = session.get('admin_id')
    
    # Filtra as bicicletas pelo administrador logado
    bicicletas = Bicicleta.query.filter_by(administrador_id=admin_id).all()
    
    return render_template('admin/bicicletas.html', bicicletas=bicicletas)

# Rota para adicionar uma bicicleta (protegida)
@admin_bp.route('/bicicletas/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_bicicleta():
    if request.method == 'POST':
        modelo = request.form['modelo']
        numero_serie = request.form['numero_serie']
        estacao_id = request.form['estacao_id']
        admin_id = session.get('admin_id')  # Obtém o ID do administrador logado

        # Verifica se o número de série já existe para o administrador logado
        if Bicicleta.query.filter_by(numero_serie=numero_serie, administrador_id=admin_id).first():
            flash('Número de série já cadastrado para o seu perfil!', 'error')
            return redirect(url_for('admin.adicionar_bicicleta'))

        nova_bicicleta = Bicicleta(modelo=modelo, numero_serie=numero_serie, estacao_id=estacao_id, administrador_id=admin_id)
        db.session.add(nova_bicicleta)
        db.session.commit()

        flash('Bicicleta adicionada com sucesso!', 'success')
        return redirect(url_for('admin.admin_bicicletas'))

    # Filtra as estações pelo administrador logado
    admin_id = session.get('admin_id')
    estacoes = Estacao.query.filter_by(administrador_id=admin_id).all()
    
    return render_template('admin/adicionar_bicicleta.html', estacoes=estacoes)

# Rota para login
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        admin = Administrador.query.filter_by(email=email).first()

        if admin and admin.check_senha(senha):
            session['admin_id'] = admin.id  # Armazena o ID do admin na sessão
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Email ou senha incorretos!', 'error')

    return render_template('admin/login.html')

# Rota para logout
@admin_bp.route('/logout')
def logout():
    session.pop('admin_id', None)  # Remove o ID do admin da sessão
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('admin.login'))


# Rota para remover uma estação
@admin_bp.route('/estacoes/remover/<int:id>', methods=['POST'])
@login_required
def remover_estacao(id):
    estacao = Estacao.query.get_or_404(id)
    
    for bicicleta in estacao.bicicletas:
        db.session.delete(bicicleta)
    
    db.session.delete(estacao)
    db.session.commit()
    flash('Estação e bicicletas associadas removidas com sucesso!', 'success')
    return redirect(url_for('admin.admin_estacoes'))

# Rota para remover uma bicicleta
@admin_bp.route('/bicicletas/remover/<int:id>', methods=['POST'])
@login_required
def remover_bicicleta(id):
    bicicleta = Bicicleta.query.get_or_404(id)
    db.session.delete(bicicleta)
    db.session.commit()
    flash('Bicicleta removida com sucesso!', 'success')
    return redirect(url_for('admin.admin_bicicletas'))

# Rota para remover um administrador
@admin_bp.route('/administradores/remover/<int:id>', methods=['POST'])
@login_required
def remover_administrador(id):
    administrador = Administrador.query.get_or_404(id)
    
    # Verifica se o administrador removido é o mesmo que está logado
    if administrador.id == session.get('admin_id'):
        session.pop('admin_id', None)  # Encerra a sessão
        flash('Você removeu sua própria conta. Por favor, faça login novamente.', 'success')
    else:
        flash('Administrador removido com sucesso!', 'success')
    
    db.session.delete(administrador)
    db.session.commit()
    return redirect(url_for('admin.admin_dashboard'))