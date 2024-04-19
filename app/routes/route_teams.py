from flask import  Blueprint, render_template, request,flash, redirect
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
            Representante = request.form["Representante"]
            SubRepresentante = request.form["SubRepresentante"]
            Email = request.form["Email"]
            Nombre_Equipo =  request.form["Nombre_Equipo"]
            Add_Equipos = Equipos(None, Representante, SubRepresentante, Email, Nombre_Equipo, None)
            Add_teams = ModeloEquipos.add_teams( Add_Equipos)
            if Add_teams != None:
                return flash('User successfully registered', 'success') ,redirect('/equipos')
            else :
                return flash('Error in the registration process ', 'danger') ,redirect('/equipos')
    else:
        """Redirección a la página principal con un mensaje de error"""
        return render_template('auth/auth.html')