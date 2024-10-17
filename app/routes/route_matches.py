from flask import Blueprint, render_template, request, redirect, url_for
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
                ORDER BY MIN(TIMESTAMP(horarios.dia, horarios.hora_inicio));""")
            data2 = cursor.fetchall()
            print(type(data2))

            cursor.execute("""
                SELECT e.grupo_id, g.nombre AS nombre_grupo, 
                    (SELECT COUNT(DISTINCT grupo_id) FROM equipos) AS total_grupos, 
                    e.id AS equipo_id, e.nombre_equipo 
                    FROM equipos e 
                    JOIN grupos g ON e.grupo_id = g.id 
                    ORDER BY e.grupo_id, e.nombre_equipo;""")
            conteo_grupo = cursor.fetchall()  # Obtener los valores

            grupos_dict = {}
            for row in conteo_grupo:
                grupo_id = row[0]
                nombre_grupo = row[1]
                total_grupos = row[2]
                equipo_id = row[3]
                nombre_equipo = row[4]
                
                # Si el grupo_id no está en el diccionario, lo agregamos con sus datos
                if grupo_id not in grupos_dict:
                    grupos_dict[grupo_id] = {
                        'grupo_id': grupo_id,
                        'nombre_grupo': nombre_grupo,
                        'total_grupos': total_grupos,
                        'equipos': []  # Inicializamos una lista vacía de equipos
                    }
                
                # Agregamos el equipo al grupo correspondiente
                grupos_dict[grupo_id]['equipos'].append({
                    'equipo_id': equipo_id,
                    'nombre_equipo': nombre_equipo
                })
            if request.method == "POST":
                # Procesar los equipos dependiendo de los grupos
                horas_por_dia = []
                for key, value in request.form.items():
                    if "_hora_inicio" in key:
                        dia = key.split("_")[0]
                        hora_inicio = value
                        hora_fin = request.form.get(f"{dia}_hora_fin")
                        if hora_inicio and hora_fin:
                            horas_por_dia.append({
                                'dia': dia,
                                'hora_inicio': hora_inicio,
                                'hora_fin': hora_fin
                            })
            # Convertimos el diccionario en una lista para pasarlo al template
            grupos = list(grupos_dict.values())
            print(grupos)
            #Ajustar la creación de `horarios` para reflejar los datos obtenidos de la consulta
            horarios = [{'nombre_equipo': row[0], 'horarios': row[1]} for row in data2]
            return render_template("partidos.html",  dates=horarios, grupos=grupos)
    else:
        """Redirección a la página principal con un mensaje de error"""
        return render_template('auth/auth.html')


