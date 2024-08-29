from flask import Flask, Blueprint, render_template
from flask_login import LoginManager,  login_user, login_required, logout_user,current_user

# from app import current_user,login_required



IndexBlueprint=Blueprint("IndexBlueprint", __name__)

@login_required
@IndexBlueprint.route('/index')
def index():
    print("usuario autenticado desde Equipos ", current_user.is_authenticated )
    if current_user.is_authenticated:
        """Listado de todos los equipos"""

        return render_template('index/index.html')
    else:
        """Redirección a la página principal con un mensaje de error"""
        return render_template('auth/auth.html')

