from flask import  Blueprint, render_template, request,flash, redirect, url_for
from flask_login import  login_required,current_user



from app.models.entities.equipos import Equipos
from app.models.modelo_equipos import ModeloEquipos

# from app import current_user,login_required



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

            Add_Equipos = Equipos(None, representante, subrepresentante, correo, nombre_equipo, None)
            print("DEsde la instancia de Equipos",Add_Equipos.correo, Add_Equipos.nombre_equipo, Add_Equipos.representante, Add_Equipos.subrepresentante)
            Add_teams = ModeloEquipos.add_teams( Add_Equipos)
            print("Addteams intancia",Add_teams)
            if Add_teams != None:
                flash('User successfully registered', 'success') 
                return render_template("Equipos.html")
            else :
                flash('Error in the registration process ', 'warning')
                return redirect(url_for('EquiposBlueprint.equipos'))
        else:
            return render_template("Equipos.html")  # Renderiza el formulario para agregar equipos
    else:
        flash('You must be logged in to access this page', 'warning')
        return redirect(url_for('AuthLogin.login'))  # Redirecciona a la página de inicio de sesión