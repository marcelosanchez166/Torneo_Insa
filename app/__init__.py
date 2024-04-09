from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager,  login_user, login_required, logout_user,current_user
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect #libreria para poder crear tokens esta se instalo con pip y generaremos tokens personalizados con la SECRET_KEY que creamos en el archivo config.py
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.modelo_usuario import ModeloUsuario
from app.database import db


# Routes Importando los Blueprints
from .routes.authorization import  auth, register
from .routes import Route_Equipos
from .routes import index
from .routes import grupos

app = Flask(__name__)



login_manager_app=LoginManager(app)#creamos una variable que hara uso de LoginManager y le pasamos la variable app que hace referencia a nuestra propia app, LoginManager 
#sirve para poder crear un administrador para nuestra app


"""El decorador @login_manager_app.user_loader llama internamente el id del usuario que se captura con el metodo login_user, luego ese id si es valido se envia hacia el metodo de clase ModeloUsuario.obtener_por_id ademas de la instancia de la base de datos """
@login_manager_app.user_loader #Se debe implementar para que se gestionen correctamente las sesiones atravez de la libreria flask_login Si no creamos el decorador login_manager_app dara este error Exception: Missing user_loader or request_loader. Refer to http://flask-login.readthedocs.io/#how-it-works for more info. cuando estemos usando login_user y Login_Manager de flask
def load_user(id):#Se creara la funcion load_user y se le pasa el id que vamos a cargar del usuario
    print("Id de la funcion loginmanager",id)
    return ModeloUsuario.obtener_por_id(id) #retornamos el metodo obtener_por_id de la clase ModeloUsuario del archivo modelousuario.py y se le pasaran dos valores la conexion a la base y el id que vamos a cargar del usuario



#Existe un ataque a formularios que se llama CSRF(Cross-site Request Forgery) (Solicitud de Falsificacion entre sitios) 
#que se enfoca en realizar peticiones al formulario que no son de nuestro sitio
"""Para evitar estos ataques podemos usar una herramienta que nos da Flask que se llama WTF que se instala con pip install Flask-WTF, con esto realizaremos es que cada 
vez que tengamos un formulario vamos a crear un token para identificarnos como los que estamos realizando las peticiones a nuestra aplicacion"""
csrf=CSRFProtect()


def init_app(config):
    # Configuration
    app.config.from_object(config)
    # Blueprints
    app.register_blueprint(auth.AuthLogin )
    app.register_blueprint(register.RegisterUser)
    app.register_blueprint(Route_Equipos.EquiposBlueprint)
    app.register_blueprint(index.IndexBlueprint)
    app.register_blueprint(grupos.gruposBlueprint)
    return app