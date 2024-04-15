from flask import Blueprint, render_template
from flask_login import  login_required,current_user

partidosBlueprint=Blueprint("partidosBlueprint", __name__)


@partidosBlueprint.route("/partidos")
@login_required
def partidos():
    print("usuario autenticado desde Equipos ", current_user.is_authenticated )
    if current_user.is_authenticated:
        """Listado de todos los equipos"""
        return render_template("partidos.html")
    else:
        """Redirección a la página principal con un mensaje de error"""
        return render_template('auth/auth.html')


