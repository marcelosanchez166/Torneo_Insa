from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import  login_required,current_user

horariosBlueprint=Blueprint("horariosBlueprint", __name__)


@horariosBlueprint.route("/horarios")
@login_required
def horarios():
    print("usuario autenticado desde Equipos ", current_user.is_authenticated )
    if current_user.is_authenticated:
        if request.method == "POST":
            dias= request.form["dias[]"]
            print(dias)
            return render_template("equipos.html")
        return render_template("horarios.html")
    else:
        """Redirección a la página principal con un mensaje de error"""
        return render_template('auth/auth.html')


