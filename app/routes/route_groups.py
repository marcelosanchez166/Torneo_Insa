from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager,  login_user, login_required, logout_user,current_user

# from app import current_user,login_required
from app.database.db import get_connection
from app.models.modelo_grupos import ModeloGrupos
from app.models.entities.grupos import Grupos


gruposBlueprint=Blueprint("gruposBlueprint", __name__)

@login_required
@gruposBlueprint.route("/grupos", methods=["GET", "POST"])
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
            if request.method == "POST":
                equipo = request.form.get("equipo")
                grupo = request.form.get("grupo")
                print(equipo, grupo)
                Egrupos = ModeloGrupos.crear_grupos(equipo, grupo)
                if Egrupos:
                    flash("Equipo agregado al grupo exitosamente", "success")
                    return redirect(url_for('gruposBlueprint.grupos'))
            else:
                flash("Error en los datos enviador", "warning")
            # cursor.execute("""SELECT  grupos.id, grupos.nombre AS grupo, GROUP_CONCAT(equipos.nombre_equipo ORDER BY equipos.nombre_equipo SEPARATOR ', ') AS equipos
            #             FROM equipos JOIN grupos ON equipos.grupo_id = grupos.id 
            #             GROUP BY grupos.nombre 
            #             ORDER BY grupos.nombre;
            #             """)
            cursor.execute("SELECT equipos.id, equipos.nombre_equipo, grupos.nombre FROM equipos JOIN  grupos ON equipos.grupo_id = grupos.id ORDER BY grupos.nombre")
            GruposE = cursor.fetchall()
            grupos_creados = [{'id' : row[0],'nombre_equipo': row[1], 'nombre_grupo': row[2]} for row in GruposE]
            #print(grupos_creados[0])
        return render_template("grupos.html", grupos=grupos, dates=horarios, equipos=equipos, grupos_creados=grupos_creados)
    else:
        """Redirección a la página principal con un mensaje de error"""
        return render_template('auth/auth.html')


#Aqui debo hacer que me redirija hacia una pantalla de editar para actualizar el id del grupo, Aqui tambien debo enviar la data a un metodo en el archivo modelo_grupos para que 
#Haga el trabajo de Actualizar el grupo en la tabla equipos
@login_required
@gruposBlueprint.route("/edit_grupos/<int:id_equipo>", methods=["GET", "POST"])
def edit_grupos(id_equipo):
    if current_user.is_authenticated:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT nombre FROM grupos ")
            grupos = [row[0] for row in cursor.fetchall()]#Extract the first value of each tuple #fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
            cursor.execute("SELECT id, nombre_equipo FROM equipos WHERE id = %s", (id_equipo,))
            equipos = cursor.fetchone()
            if request.method == "POST":
                equipo = request.form.get("equipo")
                grupo = request.form.get("grupo")
                print(equipo, grupo,"Datos que envia el cliente cuando edita el grupo del equipo")
                update_grupoid_equipo = ModeloGrupos.update_grupo(id_equipo, equipo, grupo)
                if update_grupoid_equipo:
                    flash("Grupo actualizado exitosamente", "success")
                    return redirect(url_for('gruposBlueprint.grupos'))
                flash("No se pudo actualizar el grupo del equipo", 'warning')
                return redirect(url_for("gruposBlueprint.grupos"))
            return render_template("edit_grupos.html", equipos=equipos, grupos=grupos)
    else:
        return render_template('auth/auth.html')



#El DELETE debo hacerlo como un UPDATE para que no se elimine como tal el grupo, y ademas debo enviar la data a algun metodo en el archivo modelo_grupos para que haga el trabajo
#ELIMAR(Actualizar) el grupo en la tabla equipos
@login_required
@gruposBlueprint.route("/delete_grupos/<int:id_equipo>", methods=["GET","POST"])
def delete_grupos(id_equipo):
    print(id_equipo, "ID del equipo para actualizar y poner en NULL")
    if current_user.is_authenticated:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre_equipo FROM equipos WHERE id = %s", (id_equipo,))
            data = cursor.fetchone()
            id_equipo=data[0]
            print(id_equipo)
            if data is not None:
                delete_equipos_grupo_id = ModeloGrupos.delete_grupos(id_equipo)
                if delete_equipos_grupo_id:
                    flash('El equipo ha sido eliminado exitosamente','success')
                    return redirect(url_for("gruposBlueprint.grupos"))
                flash("El grupo seleccionado no es valido", "warning")
                return redirect(url_for("gruposBlueprint.grupos"))
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
            cursor.execute("SELECT equipos.id, equipos.nombre_equipo, grupos.nombre FROM equipos JOIN  grupos ON equipos.grupo_id = grupos.id ORDER BY grupos.nombre")
            GruposE = cursor.fetchall()
            grupos_creados = [{'id' : row[0],'nombre_equipo': row[1], 'nombre_grupo': row[2]} for row in GruposE]
            print(grupos_creados[0])
            return render_template("grupos.html", grupos_creados=grupos_creados, dates=horarios)
    else:
        return render_template('auth/auth.html')
