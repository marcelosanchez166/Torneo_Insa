from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import  login_required,current_user

from app.models.modelo_horarios import Modelo_horarios
# from app.routes.route_teams import EquiposBlueprint
from app.models.entities.horarios import Horarios


from app.database.db import  get_connection

horariosBlueprint=Blueprint("horariosBlueprint", __name__)

@login_required
@horariosBlueprint.route("/horarios", methods=["POST", "GET"])
def horarios():
    if current_user.is_authenticated:
        horas_por_dia = {}
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, id_equipo, dia, hora_inicio, hora_fin FROM horarios")
            data = cursor.fetchall()

            if request.method == "POST":
                id_equipo = request.form.get('id_equipo')
                dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']
                for dia in dias:
                    dia_seleccionado = request.form.getlist(f'dias[{dia}]')
                    for d in dia_seleccionado:
                        inicio = int(request.form[f'horas[{d}][inicio]'])
                        fin = int(request.form[f'horas[{d}][fin]'])
                        if inicio < fin:
                            horas_por_dia[d] = {'inicio': inicio, 'fin': fin}
                        else:
                            flash('La hora final debe ser distinta a la inicial', 'warning')
                            return redirect(url_for("horariosBlueprint.horarios"))
                
                if horas_por_dia:
                    Modelo_horarios.agregar_horarios(horas_por_dia, id_equipo)
                    flash("Horario agregado correctamente", 'success')
                else:
                    flash("No se pudieron agregar horarios. Revise las entradas.", 'warning')
        with connection.cursor() as cursor:                    
            cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos")
            equipos = cursor.fetchall()
            cursor.execute("""
                SELECT equipos.nombre_equipo, horarios.id, horarios.id_equipo, horarios.dia, horarios.hora_inicio, horarios.hora_fin  FROM equipos 
                JOIN horarios ON equipos.id = horarios.id_equipo ORDER BY equipos.nombre_equipo
                """)
            data2 = cursor.fetchall()
            horarios = [{'id': row[1], 'nombre_equipo': row[0], 'id_equipo': row[2], 'dia': row[3], 'hora_inicio': row[4], 'hora_fin': row[5]} for row in data2]
            return render_template("horarios.html", data=data, equipos=equipos, dates=horarios)
    else:
        flash('You must be logged in to access this page', 'warning')
        return redirect(url_for('AuthLogin.login'))





@login_required
@horariosBlueprint.route("/edit_horarios/<int:id>", methods=["POST", "GET"])
def edit_horarios(id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo FROM equipos WHERE id= %s", (id,))
        data = cursor.fetchone()
        team_id = data[0]
    if request.method == "POST":
        if data is not None:
            # Procesar los horarios
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
            print(horas_por_dia)
            try:
                if len(horas_por_dia) > 0:
                    update_horarios = Modelo_horarios.actualizar_horarios( horas_por_dia, team_id)
                    flash("Equipo actualizado correctamente", "success")
                    return redirect(url_for("horariosBlueprint.horarios"))
                else:
                    flash('Debes completar todos los campos del formulario', 'warning')
                    return redirect(url_for('horariosBlueprint.edit_horarios', id=id))
            except Exception as ex:
                flash("Error al actualizar los datos del equipo", "warning")
                print("Error al actualizar los datos del equipo", ex)
        else:
            return render_template("edit_horarios.html")

    with connection.cursor() as cursor:
        cursor.execute("""SELECT 
                equipos.id, 
                equipos.nombre_equipo, 
                equipos.representante, 
                equipos.subrepresentante, 
                equipos.correo, 
                horarios.dia, 
                horarios.hora_inicio, 
                horarios.hora_fin  
                FROM equipos JOIN horarios ON equipos.id = horarios.id_equipo WHERE equipos.id = %s """, (id,))
        data2 = cursor.fetchall()

    # Construir la lista de horarios
    horarios = []
    for row in data2:
        horariodic = {
            'dia': row[5],
            'hora_inicio': row[6],
            'hora_fin': row[7]
        }
        horarios.append(horariodic)

    horario = {
        'id': data2[0][0],
        'nombre_equipo': data2[0][1],
        'representante': data2[0][2],
        'subrepresentante': data2[0][3],
        'correo': data2[0][4],
        'horarios': horarios
    }
    return render_template("edit_horarios.html", horario=horario)


@login_required
@horariosBlueprint.route('/delete_horarios/<int:id>')
def delete_horarios(id):
    print(id, "Id que recibo del frontend")
    """Elimina un equipo en base a su id"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, id_equipo, dia, hora_inicio, hora_fin FROM horarios WHERE id = %s", (id,))
        result = cursor.fetchone()
    if result is not None :
        delete_horario = Horarios(id, None, None, None, None)
        delete_horarios = Modelo_horarios.delete_horarios(delete_horario)
        if delete_horarios is not None:
            flash('El equipo ha sido eliminado exitosamente','success')
            return redirect(url_for("horariosBlueprint.horarios"))
        else:
            flash ('No se encontró el equipo que deseas borrar','warning')
            # return redirect (url_for('EquiposBlueprint.equipos'))

    with connection.cursor() as cursor:
        cursor.execute("""SELECT 
                equipos.nombre_equipo,
                horarios.id, 
                horarios.id_equipo,
                horarios.dia, 
                horarios.hora_inicio, 
                horarios.hora_fin  
                FROM equipos JOIN horarios ON equipos.id = horarios.id_equipo """)
        data2 = cursor.fetchall()

        # Construir la lista de horarios
        horarios = []
        for row in data2:
            horario = { 'id':row[1], 'nombre_equipo':row[0],'id_equipo':row[2],  'dia': row[3], 'hora_inicio': row[4], 'hora_fin': row[5]}
            horarios.append(horario)
        return render_template("horarios.html", dates=horarios)
