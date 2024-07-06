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
    print("usuario autenticado desde Equipos ", current_user.is_authenticated )
    if current_user.is_authenticated:
        horas_por_dia = {}
        connection= get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, id_equipo, dia, hora_inicio, hora_fin  FROM horarios ")
            data = cursor.fetchall()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
            #print("ID del equipo obtenido",id_equipo)
            if data:
                id_equipo1 = data[0][1]
                print("ID del equipo obtenido", id_equipo1)
            else:
                id_equipo1 = None
                print("No se encontraron horarios")

            if request.method == "POST":
                id_equipo = request.form.getlist( 'id_equipo' )
                dia_lunes = request.form.getlist( 'dias[lunes]' )
                for dia in dia_lunes:
                    inicio =int(request.form['horas[{}][inicio]'.format(dia)])
                    # print(type(inicio), "miercoles")
                    fin =  int(request.form['horas[{}][fin]'.format(dia) ])
                    if  inicio < fin:
                        horas_por_dia[dia] = {'inicio': inicio, 'fin': fin}
                    else:
                        flash('La hora final debe ser distinta a la inicial', 'warning')
                        return redirect(url_for( "EquiposBlueprint.equipos" ))
                    print("Imprimiendo el dia y las horas ",dia,horas_por_dia[dia])

                dia_martes = request.form.getlist( 'dias[martes]' )
                for dia in dia_martes:
                    inicio =int(request.form['horas[{}][inicio]'.format(dia)])
                    # print(type(inicio), "miercoles")
                    fin =  int(request.form['horas[{}][fin]'.format(dia) ])
                    if  inicio < fin:
                        horas_por_dia[dia] = {'inicio': inicio, 'fin': fin}
                    else:
                        flash('La hora final debe ser distinta a la inicial', 'warning')
                        return redirect(url_for( "EquiposBlueprint.equipos" ))
                    print("Imprimiendo el dia y las horas ",dia,horas_por_dia[dia])

                dia_miercoles = request.form.getlist('dias[miercoles]')
                for dia in dia_miercoles:
                    inicio =int(request.form['horas[{}][inicio]'.format(dia)])
                    # print(type(inicio), "miercoles")
                    fin =  int(request.form['horas[{}][fin]'.format(dia) ])
                    if  inicio < fin:
                        horas_por_dia[dia] = {'inicio': inicio, 'fin': fin}
                    else:
                        flash('La hora final debe ser distinta a la inicial', 'warning')
                        return redirect(url_for( "EquiposBlueprint.equipos" ))
                    print("Imprimiendo el dia y las horas ",dia,horas_por_dia[dia])

                dia_jueves= request.form.getlist('dias[jueves]')
                for dia in dia_jueves:
                    inicio =int(request.form['horas[{}][inicio]'.format(dia)])
                    # print(type(inicio), "miercoles")
                    fin =  int(request.form['horas[{}][fin]'.format(dia) ])
                    if  inicio < fin:
                        horas_por_dia[dia] = {'inicio': inicio, 'fin': fin}
                    else:
                        flash('La hora final debe ser distinta a la inicial', 'warning')
                        return redirect(url_for( "EquiposBlueprint.equipos" ))
                    print("Imprimiendo el dia y las horas ",dia,horas_por_dia[dia])

                dia_viernes = request.form.getlist('dias[viernes]')
                for dia in dia_viernes:
                    inicio =int(request.form['horas[{}][inicio]'.format(dia)])
                    # print(type(inicio), "miercoles")
                    fin =  int(request.form['horas[{}][fin]'.format(dia) ])
                    if  inicio < fin:
                        horas_por_dia[dia] = {'inicio': inicio, 'fin': fin}
                    else:
                        flash('La hora final debe ser distinta a la inicial', 'warning')
                        return redirect(url_for( "EquiposBlueprint.equipos" ))
                    print("Imprimiendo el dia y las horas virnesssss ",dia,horas_por_dia[dia])

                print(horas_por_dia, "diccionario de los dias y horas ")
                horariosmodel= Modelo_horarios.agregar_horarios(horas_por_dia,id_equipo)
                if len(horas_por_dia) >0:
                    if horariosmodel:
                        flash("Horario agregado correctamente")
                else:
                    """Redirección a la página principal con un mensaje de error"""
                    return render_template('horarios.html')
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos ")
            equipos = cursor.fetchall()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
            #print(type(equipos, "Lista de equipos"))  # Esto imprimirá los equipos en la consola
            return render_template("horarios.html", data=data, equipos=equipos)
    else:
        flash('You must be logged in to access this page', 'warning')
        return redirect(url_for('AuthLogin.login'))  # Redirecciona a la página de inicio de sesión




