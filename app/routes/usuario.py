from flask import Blueprint, render_template

# Cria um Blueprint para as rotas do usuário
usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

@usuario_bp.route('/home')
def home():
    return render_template('usuario/home.html')

@usuario_bp.route('/alugar')
def alugar():
    return render_template('usuario/alugar.html')

@usuario_bp.route('/perfil')
def perfil():
    return render_template('usuario/perfil.html')