from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager,  login_user, login_required, logout_user,current_user

# from app import current_user,login_required
from app.database.db import get_connection


gruposBlueprint=Blueprint("gruposBlueprint", __name__)

@login_required
@gruposBlueprint.route("/grupos")
def grupos():
    print("usuario autenticado desde Equipos ", current_user.is_authenticated )
    if current_user.is_authenticated:
        connection= get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT nombre FROM grupos ")
            grupos = [row[0] for row in cursor.fetchall()]#Extract the first value of each tuple #fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
            cursor.execute("SELECT nombre_equipo FROM equipos")
            equipos = [row[0] for row in cursor.fetchall()]  # Extract the first value of each tuple
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

        return render_template("grupos.html", grupos=grupos, dates=horarios, equipos=equipos)
    else:
        """Redirección a la página principal con un mensaje de error"""
        return render_template('auth/auth.html')


@login_required
@gruposBlueprint.route("/edit_grupos/<int:grupo_id>", methods=["GET", "POST"])
def edit_grupos(grupo_id):
    if current_user.is_authenticated:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM grupos WHERE id_grupo = %s", (grupo_id,))
            data = cursor.fetchone()
            if request.method == "POST":
                nombre_grupo = request.form.get("nombre_grupo")
                # descripcion_grupo = request.form.get("descripcion_grupo")
                cursor.execute("UPDATE grupos SET nombre = %s, WHERE id = %s",(grupo_id,))
                connection.commit()
                return redirect(url_for("gruposBlueprint.grupos"))
            return render_template("edit_grupos.html", grupo=data)
    else:
        return render_template('auth/auth.html')
    

