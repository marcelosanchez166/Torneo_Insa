from flask import Blueprint, render_template
from flask_login import  login_required,current_user

partidosBlueprint=Blueprint("gruposBlueprint", __name__)


@partidosBlueprint.route("/Grupo")
@login_required
def grupo():
    print("usuario autenticado desde Equipos ", current_user.is_authenticated )
    if current_user.is_authenticated:
        """Listado de todos los equipos"""
        return render_template("partidos.html")
    else:
        """Redirección a la página principal con un mensaje de error"""
        return render_template('auth/auth.html')
