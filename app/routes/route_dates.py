from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import  login_required,current_user

from app.models.modelo_horarios import Modelo_horarios
# from app.routes.route_teams import EquiposBlueprint

horariosBlueprint=Blueprint("horariosBlueprint", __name__)


@horariosBlueprint.route("/horarios")
@login_required
def horarios():
    print("usuario autenticado desde Equipos ", current_user.is_authenticated )
    if current_user.is_authenticated:
        flash("Bienvenido a Horarios", "success")
        # if horarios is not None:
        #     enviar_horarios = Modelo_horarios.agregar_horarios(horarios, id_equipo)
        #     if enviar_horarios is not None:
        #         return redirect(url_for("EquiposBlueprint.equipos"))
        # else:
        #     #Si no hay equipos en la URL redirecciona a la pagina de los equipos
        #     return redirect(url_for('EquiposBlueprint.equipos'))
    else:
        """Redirección a la página principal con un mensaje de error"""
        return render_template('auth/auth.html')


