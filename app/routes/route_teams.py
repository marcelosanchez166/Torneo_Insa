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
            cursor.execute("SELECT nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos ")
            data = cursor.fetchall()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
            print(data[0])
            return render_template("Equipos.html", data=data)
    else:
        flash('You must be logged in to access this page', 'warning')
        return redirect(url_for('AuthLogin.login'))  # Redirecciona a la página de inicio de sesión