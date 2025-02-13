from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Usuario
from app import db
from functools import wraps


user_bp = Blueprint('user', __name__, url_prefix='/user')

# Decorator para verificar se o usuário está logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'error')
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function

# Rota para cadastrar um usuário
@user_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']


        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'error')
            return redirect(url_for('user.cadastrar_usuario'))


        novo_usuario = Usuario(nome=nome, email=email)
        novo_usuario.set_senha(senha)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('user.login'))

    return render_template('user/cadastrar_usuario.html')


# Rota para o login de usuário
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_senha(senha):
            session['usuario_id'] = usuario.id
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('user.dashboard'))
        else:
            flash('Email ou senha incorretos!', 'error')

    return render_template('user/login.html')


# Rota para logout
@user_bp.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('user.login'))


@user_bp.route('/dashboard')
@login_required
def dashboard():
    usuario_id = session.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    return render_template('user/dashboard.html', usuario=usuario)