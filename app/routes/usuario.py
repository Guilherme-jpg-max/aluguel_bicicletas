from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Usuario
from app import db
from functools import wraps
from datetime import datetime, timedelta
from app.models import Usuario, Estacao, Bicicleta, Aluguel


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

        if not usuario:
            flash('Usuário não encontrado!', 'error')
            return redirect(url_for('user.login'))

        if not usuario.check_senha(senha):
            flash('Email ou senha incorretos!', 'error')
            return redirect(url_for('user.login'))

        session['usuario_id'] = usuario.id  # Salva ID do usuário na sessão
        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('user.dashboard'))

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
    estacoes = Estacao.query.all()

    bicicletas_disponiveis = Bicicleta.query.filter_by(status='disponivel').all()


    aluguels_ativos = Aluguel.query.filter_by(usuario_id=usuario.id, data_fim=None).limit(3).all()

    return render_template('user/dashboard.html', usuario=usuario, estacoes=estacoes, bicicletas=bicicletas_disponiveis, aluguels_ativos=aluguels_ativos, timedelta=timedelta)



@user_bp.route('/alugar/<int:estacao_id>/<int:bicicleta_id>', methods=['POST'])
@login_required
def alugar_bicicleta(estacao_id, bicicleta_id):
    usuario_id = session.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        flash('Usuário não encontrado!', 'error')
        return redirect(url_for('user.dashboard'))

    aluguels_ativos = Aluguel.query.filter_by(usuario_id=usuario.id, data_fim=None).all()

    if len(aluguels_ativos) >= 3:
        flash('Você já tem 3 aluguéis ativos. Não é possível alugar mais bicicletas.', 'error')
        return redirect(url_for('user.dashboard'))

    if aluguels_ativos and any(aluguel.bicicleta.estacao_id != estacao_id for aluguel in aluguels_ativos):
        flash('Você só pode alugar bicicletas na mesma estação das já alugadas.', 'error')
        return redirect(url_for('user.dashboard'))

    bicicleta = Bicicleta.query.filter_by(id=bicicleta_id, estacao_id=estacao_id, status='disponivel').first()

    if not bicicleta:
        flash('Bicicleta não disponível!', 'error')
        return redirect(url_for('user.dashboard'))

    tempo_horas = int(request.form['tempo_horas'])
    preco_por_hora = 5.0
    valor_total = tempo_horas * preco_por_hora

    if usuario.saldo < valor_total:
        flash('Saldo insuficiente para alugar esta bicicleta.', 'error')
        return redirect(url_for('user.dashboard'))

    usuario.saldo -= valor_total
    bicicleta.status = 'alugada'

    aluguel = Aluguel(usuario_id=usuario.id, bicicleta_id=bicicleta.id, administrador_id=1)
    db.session.add(aluguel)
    db.session.commit()

    flash(f'Bicicleta {bicicleta.modelo} alugada com sucesso por {tempo_horas} horas!', 'success')
    return redirect(url_for('user.dashboard'))




@user_bp.route('/bicicletas/<int:estacao_id>')
@login_required
def listar_bicicletas_por_estacao(estacao_id):
    estacao = Estacao.query.get_or_404(estacao_id)
    bicicletas = Bicicleta.query.filter_by(estacao_id=estacao.id).all()

    return render_template('user/listar_bicicletas.html', estacao=estacao, bicicletas=bicicletas)


@user_bp.route('/adicionar_saldo', methods=['GET', 'POST'])
@login_required
def adicionar_saldo():
    usuario_id = session.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    if request.method == 'POST':
        valor_adicionado = float(request.form['valor'])

        if valor_adicionado <= 0:
            flash('Valor inválido!', 'error')
            return redirect(url_for('user.adicionar_saldo'))

        usuario.saldo += valor_adicionado
        db.session.commit()

        flash(f'Saldo adicionado com sucesso! Seu novo saldo é R${usuario.saldo:.2f}', 'success')
        return redirect(url_for('user.dashboard'))

    return render_template('user/adicionar_saldo.html')


@user_bp.route('/devolver/<int:aluguel_id>', methods=['POST'])
@login_required
def devolver_bicicleta(aluguel_id):
    usuario_id = session.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    aluguel = Aluguel.query.get_or_404(aluguel_id)
    bicicleta = aluguel.bicicleta

    if aluguel.usuario_id != usuario.id:
        flash('Você não tem permissão para devolver esta bicicleta.', 'error')
        return redirect(url_for('user.dashboard'))

    if bicicleta.status == 'disponivel':
        flash('Esta bicicleta já foi devolvida.', 'error')
        return redirect(url_for('user.dashboard'))

    # O usuário escolhe a estação onde deseja devolver a bicicleta
    estacao_id = int(request.form['estacao_id'])
    estacao = Estacao.query.get(estacao_id)

    if not estacao:
        flash('Estação inválida!', 'error')
        return redirect(url_for('user.dashboard'))

    bicicleta.status = 'disponivel'
    bicicleta.estacao_id = estacao_id 
    aluguel.data_fim = datetime.utcnow()

    if aluguel.data_fim < aluguel.data_inicio:
        flash('Data de devolução inválida.', 'error')
        return redirect(url_for('user.dashboard'))

    tempo_aluguel = (aluguel.data_fim - aluguel.data_inicio).total_seconds() / 3600  # em horas

    if bicicleta.valor_por_hora: 
        valor_total = tempo_aluguel * bicicleta.valor_por_hora
    else:
        flash('Valor por hora não disponível para esta bicicleta.', 'error')
        return redirect(url_for('user.dashboard'))

    aluguel.valor_total = valor_total
    db.session.commit()

    flash(f'Bicicleta {bicicleta.modelo} devolvida com sucesso na estação {estacao.nome}!', 'success')

    return redirect(url_for('user.dashboard'))