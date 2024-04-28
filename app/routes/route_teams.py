from flask import  Blueprint, render_template, request,flash, redirect, url_for
from flask_login import  login_required,current_user


from app.models.entities.equipos import Equipos
from app.models.modelo_equipos import ModeloEquipos
from app.database.db import  get_connection


EquiposBlueprint=Blueprint("EquiposBlueprint", __name__)

@login_required
@EquiposBlueprint.route("/equipos", methods=["GET", "POST"])
def equipos():
    print("usuario autenticado desde Equipos ", current_user.is_authenticated )
    if current_user.is_authenticated:
        if request.method == "POST":
            representante = request.form["Representante"]
            subrepresentante = request.form["SubRepresentante"]
            correo = request.form["Email"]
            nombre_equipo =  request.form["Nombre_Equipo"]
            print(representante,subrepresentante,correo,nombre_equipo)

            # hora_inicio_lunes = request.form['horas[lunes][inicio]']
            # print(hora_inicio_lunes, "hora inicio lunes")
            # hora_fin_lunes = request.form['horas[lunes][fin]']
            # print(hora_fin_lunes, "hora fin lunes")
            # dia = request.form['dias[lunes]']
            # print(dia, "chekeado")

            dia_lunes = request.form.getlist( 'dias[lunes]' )
            horas_por_dia = {}
            for i in dia_lunes:
                print(i, 'Valor de la lista que se obtiene del formulario')
            print(type(dia_lunes))
            for dia in dia_lunes:
                inicio = request.form['horas[{}][inicio]'.format(dia)]
                fin = request.form['horas[{}][fin]'.format(dia)]
                horas_por_dia[dia] = {'inicio': inicio, 'fin': fin}
                print("Imprimiendo el dia y las horas ",dia,horas_por_dia[dia])

            dia_martes = request.form.getlist( 'dias[martes]' )
            horas_por_dia = {}
            for i in dia_martes:
                print(i, 'Valor de la lista que se obtiene del formulario')
            print(type(dia_martes))
            for dia in dia_martes:
                inicio = request.form['horas[{}][inicio]'.format(dia)]
                fin = request.form['horas[{}][fin]'.format(dia)]
                horas_por_dia[dia] = {'inicio': inicio, 'fin': fin}
                print("Imprimiendo el dia y las horas ",dia,horas_por_dia[dia])

            Add_Equipos = Equipos(None,nombre_equipo, representante, subrepresentante, correo,  None)
            print("DEsde la instancia de Equipos",Add_Equipos.correo, Add_Equipos.nombre_equipo, Add_Equipos.representante, Add_Equipos.subrepresentante)
            Add_teams = ModeloEquipos.add_teams( Add_Equipos)
            #print("Addteams intancia valor",Add_teams)
            if Add_teams is not None:
                flash('User successfully registered', 'success')
                    # return render_template("Equipos.html")
            else :
                flash('Error in the registration process ', 'warning')
                return redirect(url_for('EquiposBlueprint.equipos'))
        connection= get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos ")
            data = cursor.fetchall()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
            print(data[0])
            return render_template("Equipos.html", data=data)
    else:
        flash('You must be logged in to access this page', 'warning')
        return redirect(url_for('AuthLogin.login'))  # Redirecciona a la página de inicio de sesión
    

@EquiposBlueprint.route("/edit_equipo/<int:id>", methods=["POST", "GET"])
def  edit_equipo():
    if current_user.is_authenticated:
        connection= get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos ")
            data = cursor.fetchone()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
            print(data[0], data[1], data, "Data obtenida del select de edit_team")
        if request.method == "POST":
            if data is not None:
                nombre_equipo = request.form['nombre_equipo']
                representante = request.form['representante']
                subrepresentante = request.form['subrepresentante']
                correo = request.form["correo"]
                grupo_id = request.form["grupo_id"]
                print("Entro al post desde el formulario el nombre nuevo de la tarea", nombre_equipo, representante, subrepresentante, correo, grupo_id)
                update = Equipos(data[0], nombre_equipo, representante, subrepresentante, correo, grupo_id)
                print(update.id, update.nombre_equipo, update.representante, update.subrepresentante, update.correo, update.grupo_id, "lo que se le envia a la clase Equipos \n")
            try:
                update_equipos = ModeloEquipos.update_equipos(update) 
                if update_equipos is  not None:#Pregunto si la instancia del metodo de clase es diferente de None entonces que envie un mensaje flash diciendo que se elimino la tarea ya que el proceso de eliminacion se hara en el metodo de instancia de  ModeloTareas.delete_tarea
                    flash("Equipos Actualizado correctamente", "success")
                    return redirect(url_for("EquiposBlueprint.equipos"))
                else:
                    flash("Error actualizando el equipo", "warning")#Si la eliminacion de la tarea en el metodo de clase  ModeloTareas.delete_tarea falla se mostrara este msj
            except  Exception as ex:
                print ("Error al actualizar los datos del equipo",ex)
        return render_template("edit_equipos.html")
        # Obtener todas las tareas asociadas al usuario después de eliminar la tarea en el metodo de clase  ModeloTareas.delete_tarea, esta nueva lista de tareas se envia con la renderizacion de la plantilla task.html de la siguiente forma return render_template("task.html", send_tasks=send_tasks)
    connection= get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos ")
        data = cursor.fetchall()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
        print(data[0])
    return render_template("edit_task.html", sends_teams = data )
