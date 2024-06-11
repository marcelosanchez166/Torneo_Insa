from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import  login_required,current_user

from app.models.modelo_horarios import Modelo_horarios
# from app.routes.route_teams import EquiposBlueprint
from app.models.entities.horarios import Horarios


from app.database.db import  get_connection

horariosBlueprint=Blueprint("horariosBlueprint", __name__)


@horariosBlueprint.route("/horarios", methods=["POST", "GET"])
@login_required
def horarios():
    print("usuario autenticado desde Equipos ", current_user.is_authenticated )
    if current_user.is_authenticated:
        connection= get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos ")
            data = cursor.fetchall()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
        if request.method == "POST":
            dia = request.form["Dia"]
            hora_inicio = request.form["hora_inicio"]
            hora_fin = request.form["hora_fin "]
            add_horarios = Horarios()
        else:
            """Redirección a la página principal con un mensaje de error"""
            return render_template('auth/auth.html')
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, id_equipo, dia, hora_inicio, hora_fin  FROM horarios ")
            data = cursor.fetchall()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
            return render_template("horarios.html", data=data)
    else:
        flash('You must be logged in to access this page', 'warning')
        return redirect(url_for('AuthLogin.login'))  # Redirecciona a la página de inicio de sesión


