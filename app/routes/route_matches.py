from flask import Blueprint, render_template
from flask_login import  login_required,current_user
from app.database.db import get_connection

partidosBlueprint=Blueprint("partidosBlueprint", __name__)


@partidosBlueprint.route("/partidos", methods=['POST', 'GET'])
@login_required
def partidos():
    print("usuario autenticado desde Equipos ", current_user.is_authenticated )
    if current_user.is_authenticated:
        connection= get_connection()
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
                ORDER BY MIN(TIMESTAMP(horarios.dia, horarios.hora_inicio));
            """)
            data2 = cursor.fetchall()
            #Ajustar la creación de `horarios` para reflejar los datos obtenidos de la consulta
            horarios = [{'nombre_equipo': row[0], 'horarios': row[1]} for row in data2]
            return render_template("partidos.html",  dates=horarios)
    else:
        """Redirección a la página principal con un mensaje de error"""
        return render_template('auth/auth.html')


