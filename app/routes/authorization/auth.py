from flask_login import LoginManager,  login_user, login_required, logout_user,current_user 
from flask import current_app as app #Importando el archivo de configuracion de nuestra aplicacion current_app hace referencia a nuestra app actual 
from flask import render_template, redirect, url_for, flash,request
from flask import Blueprint


from app.models.modelo_usuario  import ModeloUsuario
from app.models.entities.usuario import Usuario
from app.routes.Route_Equipos import EquiposBlueprint, equipos


from app.database.db import get_connection as db


AuthLogin = Blueprint("AuthLogin", __name__)




@AuthLogin.route("/")
def index():
    return redirect(url_for("AuthLogin.login"))

@AuthLogin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(password,"Imprimiendo lo que se le envia desde el formulario en la password")
        #encriptado = generate_password_hash(password, method='pbkdf2:sha256')
        usuario = Usuario(None, username, password, None )
        #usuario = Usuario(None, request.form["username"], request.form["password"], None )
        print(usuario.password, "dato de la password cuando se crea la instancia", usuario.username)
        usuario_logueado=ModeloUsuario.login(usuario)
        print("Usuario logueado en app", usuario_logueado)
        if  usuario_logueado !=  None:
                login_user(usuario_logueado)#Utilizando el modulo logQin_user de flask para poder loguear al usuario que se devuelve como inicio de sesion exitoso sirve para ver la sesion del usuario que se ha logueado
                print("Ingresando al index porque el logue fue exitoso" )
                print("usuario actual de", usuario_logueado )
                return redirect( url_for( 'IndexBlueprint.index'))#El render_template tambien sirve para dirigir a otra plantilla pero cuando pero para este caso es mejor el redirect ya que funciona como redireccionamiento
        else:
            return render_template("auth/auth.html")
    else:
        return render_template("auth/auth.html")
    



# Ruta para cerrar sesión
@AuthLogin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Session closed', 'info')
    return redirect(url_for('AuthLogin.login'))
