from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.database.db import get_connection

from app.models.modelo_partidos import Modelo_partidos
from app.models.entities.partidos import Partidos

partidosBlueprint = Blueprint("partidosBlueprint", __name__)


@partidosBlueprint.route("/partidos", methods=['POST', 'GET'])
@login_required
def partidos():
    print("usuario autenticado desde Partidos ", current_user.is_authenticated)
    if current_user.is_authenticated:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    equipos.nombre_equipo,
                    GROUP_CONCAT(
                        CONCAT(horarios.dia, ' ', horarios.hora_inicio, '-', horarios.hora_fin) 
                        ORDER BY horarios.dia, horarios.hora_inicio SEPARATOR ', '
                    ) AS horarios
                FROM equipos
                JOIN horarios ON equipos.id = horarios.id_equipo
                GROUP BY equipos.nombre_equipo
                ORDER BY MIN(TIMESTAMP(horarios.dia, horarios.hora_inicio));""")
            data2 = cursor.fetchall()
            # print(type(data2))

            cursor.execute("""
                    SELECT g.id AS grupo_id, g.nombre AS nombre_grupo, 
                        e.id AS equipo_id, e.nombre_equipo 
                    FROM grupos g
                    JOIN equipos e ON e.grupo_id = g.id 
                    ORDER BY g.id, e.nombre_equipo;
                """)
            data = cursor.fetchall()

            # Organizar datos por grupos
            grupos = {}
            for grupo_id, nombre_grupo, equipo_id, nombre_equipo in data:
                if grupo_id not in grupos:
                    grupos[grupo_id] = {
                        "nombre_grupo": nombre_grupo, "equipos": []}
                grupos[grupo_id]["equipos"].append(
                    {"id": equipo_id, "nombre": nombre_equipo})

            if request.method == 'POST':
                # Procesar el formulario enviado
                grupo_id = request.form.get("grupo")
                id_equipo_local = request.form.get("equipo1")
                id_equipo_visitante = request.form.get("equipo2")
                date = request.form.get("fecha_hora")
                print(grupo_id, id_equipo_local, id_equipo_visitante)
                Egrupos = Partidos(None, id_equipo_local,id_equipo_visitante, date, grupo_id)
                print(Egrupos.id_equipo_local, Egrupos.id_equipo_visitante,Egrupos.date, Egrupos.grupo_id,  "Desde routeMatches")
                partido_registrado = Modelo_partidos.agregar_partido(Egrupos)
                if partido_registrado:
                    flash("Partido agregado al grupo exitosamente", "success")
                    return redirect(url_for('partidosBlueprint.partidos'))
            # Ajustar la creación de `horarios` para reflejar los datos obtenidos de la consulta
            horarios = [{'nombre_equipo': row[0], 'horarios': row[1]}
                        for row in data2]
            return render_template("partidos.html",  dates=horarios, grupos=grupos)
    else:
        """Redirección a la página principal con un mensaje de error"""
        return render_template('auth/auth.html')


@partidosBlueprint.route("/equipos/<int:grupo_id>", methods=['GET'])
@login_required
def obtener_equipos(grupo_id):
    if current_user.is_authenticated:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, nombre_equipo 
                FROM equipos 
                WHERE grupo_id = %s
                ORDER BY nombre_equipo
            """, (grupo_id,))
            equipos = [{"id": row[0], "nombre": row[1]}
                       for row in cursor.fetchall()]
        return jsonify(equipos)
    else:
        return jsonify({"error": "Usuario no autenticado"}), 401
