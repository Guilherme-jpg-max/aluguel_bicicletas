from flask import Blueprint, redirect, url_for

main_bp = Blueprint('main', __name__)

# Rota raiz do aplicativo (corresponde a /)
@main_bp.route('/')
def index():
    return redirect(url_for('user.cadastrar_usuario'))
