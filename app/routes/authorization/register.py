from flask_login import LoginManager,  login_user, login_required, logout_user,current_user as app
from flask import current_app#Importando el archivo de configuracion de nuestra aplicacion current_app hace referencia a nuestra app actual 
from flask import render_template, redirect, url_for, flash,request
from flask import Blueprint

from app.models.modelo_usuario import ModeloUsuario
from app.models.entities.usuario import Usuario



from app.database.db import get_connection as db




RegisterUser = Blueprint("RegisterUser", __name__)


@RegisterUser.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        #password = generate_password_hash(password)
        email = request.form["email"]
        print(username, password, email, "lo que se envia en el formulario \n")
        usuario_re = Usuario(None, username, password, email)
        print(usuario_re.username, usuario_re.password, usuario_re.email, "lo que se le envia a la clase USUARIO \n")
        user_register = ModeloUsuario.RegisterUser(usuario_re)
        print("Hola",user_register, "lo que se le envia a la clase MODELOUSUARIO con el Metodo REgisterUser \n")
        if user_register  is not None:
            flash('User successfully registered', 'success')
            return redirect(url_for('AuthLogin.login'))
        else:
            flash('error registering user', 'warning')
            return render_template('auth/register.html')
    return render_template("auth/register.html")
