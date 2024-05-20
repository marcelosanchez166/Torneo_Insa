from flask import  Blueprint, render_template, request,flash, redirect, url_for
from flask_login import  login_required,current_user


from app.models.entities.equipos import Equipos
from app.models.modelo_equipos import ModeloEquipos
from app.database.db import  get_connection

from app.models.modelo_horarios import Modelo_horarios



EquiposBlueprint=Blueprint("EquiposBlueprint", __name__)

@login_required
@EquiposBlueprint.route("/equipos", methods=["GET", "POST"])
def equipos():
    horas_por_dia = {}
    print("usuario autenticado desde Equipos ", current_user.is_authenticated )
    if current_user.is_authenticated:
        if request.method == "POST":
            representante = request.form["Representante"]
            subrepresentante = request.form["SubRepresentante"]
            correo = request.form["Email"]
            nombre_equipo =  request.form["Nombre_Equipo"]
            print(representante,subrepresentante,correo,nombre_equipo)


            dia_lunes = request.form.getlist( 'dias[lunes]' )
            for dia in dia_lunes:
                inicio =int(request.form['horas[{}][inicio]'.format(dia)])
                # print(type(inicio), "miercoles")
                fin =  int(request.form['horas[{}][fin]'.format(dia) ])
                if  inicio < fin:
                    horas_por_dia[dia] = {'inicio': inicio, 'fin': fin}
                else:
                    flash('La hora final debe ser distinta a la inicial', 'error')
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
                    flash('La hora final debe ser distinta a la inicial', 'error')
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
                    flash('La hora final debe ser distinta a la inicial', 'error')
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
                    flash('La hora final debe ser distinta a la inicial', 'error')
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
                    flash('La hora final debe ser distinta a la inicial', 'error')
                    return redirect(url_for( "EquiposBlueprint.equipos" ))
                print("Imprimiendo el dia y las horas virnesssss ",dia,horas_por_dia[dia])

            print(horas_por_dia, "diccionario de los dias y horas ")
            Add_Equipos = Equipos(None,nombre_equipo, representante, subrepresentante, correo,  None)
            if Add_Equipos:
                print("DEsde la instancia de Equipos",Add_Equipos.correo, Add_Equipos.nombre_equipo, Add_Equipos.representante, Add_Equipos.subrepresentante)
                if len(horas_por_dia) >0:
                    Add_teams = ModeloEquipos.add_teams(horas_por_dia,Add_Equipos)
                    # if Add_teams is not None:
                    #     flash('Equipo registrado', 'success')
                    # else :
                    #     flash('Error in the registration process ', 'warning')
                    #     return redirect(url_for('EquiposBlueprint.equipos'))
                else:
                    flash('Debes completar todos los capos del formulario', 'error')
                    return redirect(url_for('EquiposBlueprint.equipos'))
        connection= get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos ")
            data = cursor.fetchall()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
            return render_template("Equipos.html", data=data)
    else:
        flash('You must be logged in to access this page', 'warning')
        return redirect(url_for('AuthLogin.login'))  # Redirecciona a la página de inicio de sesión



@login_required
@EquiposBlueprint.route("/edit_equipo/<int:id>", methods=["POST", "GET"])
def edit_equipo(id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos  WHERE id= %s", (id) )
        data = cursor.fetchone()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
        #print(data[0], data[1], data, "Data obtenida del select de edit_team")
    if request.method == "POST":
        if data is not None:
            nombre_equipo = request.form['nombre_equipo']
            representante = request.form['representante']
            subrepresentante = request.form['subrepresentante']
            correo = request.form["correo"]
            #grupo_id = request.form["grupo_id"]
            print("Entro al post desde el formulario el nombre nuevo de la tarea", nombre_equipo, representante, subrepresentante, correo, None)
            update = Equipos(id, nombre_equipo, representante, subrepresentante, correo, None)
            print(update.id, update.nombre_equipo, update.representante, update.subrepresentante, update.correo, None, "lo que se le envia a la clase Equipos \n")
            try:
                update_equipos = ModeloEquipos.update_equipos(update) 
                if update_equipos is  not None:#Pregunto si la instancia del metodo de clase es diferente de None entonces que envie un mensaje flash diciendo que se elimino la tarea ya que el proceso de eliminacion se hara en el metodo de instancia de  ModeloTareas.delete_tarea
                    flash("Equipo actualizado correctamente", "success")
                    return redirect(url_for("EquiposBlueprint.equipos"))
                else:
                    flash("Error actualizando el equipo", "warning")#Si la eliminacion de la tarea en el metodo de clase  ModeloTareas.delete_tarea falla se mostrara este msj
            except  Exception as ex:
                flash("Error al actualizar los datos del equipo", "warning")
                print ("Error al actualizar los datos del equipo",ex)
        else:
            return render_template("edit_equipos.html")
    # Obtener todas las tareas asociadas al usuario después de eliminar la tarea en el metodo de clase  ModeloTareas.delete_tarea, esta nueva lista de tareas se envia con la renderizacion de la plantilla task.html de la siguiente forma return render_template("task.html", send_tasks=send_tasks)
    connection= get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos WHERE id = %s ",(id,))
        data2 = cursor.fetchall()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
        print(data[0])
    return render_template("edit_equipos.html", sends_teams = data2 )




@login_required
@EquiposBlueprint.route('/delete_equipo/<int:id>')
def delete_equipo(id):
    """Elimina un equipo en base a su id"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo FROM equipos WHERE id = %s", (id,))
        result = cursor.fetchone()
    if result is not None :
        delete_equipo = Equipos(id, None, None, None, None, None)
        delete_equipos = ModeloEquipos.delete_equipos(delete_equipo)
        if delete_equipos is not None:
            flash('El equipo ha sido eliminado exitosamente','success')
            return redirect(url_for("EquiposBlueprint.equipos"))
        else:
            flash ('No se encontró el equipo que deseas borrar','warning')
            # return redirect (url_for('EquiposBlueprint.equipos'))
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id  FROM equipos")
        data = cursor.fetchall()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
        print(data[0])
        return render_template("Equipos.html", data=data)
    # return redirect(url_for("EquiposBlueprint.equipos"))