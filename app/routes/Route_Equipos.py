from flask import Flask, Blueprint, render_template
from flask_login import LoginManager,  login_user, login_required, logout_user,current_user

# from app import current_user,login_required



EquiposBlueprint=Blueprint("EquiposBlueprint", __name__)

@login_required
@EquiposBlueprint.route("/equipos")
def equipos():
    print("usuario autenticado desde Equipos ", current_user.is_authenticated )
    if current_user.is_authenticated:
        """Listado de todos los equipos"""
        return render_template("Equipos.html")
    else:
        """Redirección a la página principal con un mensaje de error"""
        return render_template('auth/auth.html')