from flask import  Blueprint, render_template, request
from flask_login import  login_required,current_user

# from app import current_user,login_required



EquiposBlueprint=Blueprint("EquiposBlueprint", __name__)

@login_required
@EquiposBlueprint.route("/equipos", method=("POST", "GET"))
def equipos():
    print("usuario autenticado desde Equipos ", current_user.is_authenticated )
    if current_user.is_authenticated:
        if request.method == "POST":
            Representante = request.form["Representante"]
            SubRepresentante = request.form["SubRepresentante"]
            Email = request.form["Email"]
            Nombre_Equipo =  request.form["Nombre_Equipo"]
        """Listado de todos los equipos"""
        return render_template("equipos.html")
    else:
        """Redirección a la página principal con un mensaje de error"""
        return render_template('auth/auth.html')