#Creacion de clase para la tabla jugadores en la cual podriamos realizar CRUD de los tipos de usuarios que puede haber en la app 
from werkzeug.security import generate_password_hash, check_password_hash #Importando los metodos para encriptar y desencriptar las passwords, metodo para desencriptar(check_password_hash),metodo para encriptar(generate_password_hash)
from flask_login import UserMixin



class Usuario(UserMixin):#Esta clase hereda de la clase UserMixin del paquete flask_login por eso hay que importarlo ya que necesita tener el atributo is_active que tienen la clase UserMixin para las sesiones 
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password    
        self.email = email


    def __str__(self):
        return f"Usuario(id={self.id}, username={self.username}, password={self.password}, email={self.email})"

    def get_id(self):
        return str(self.id)

    @classmethod#Convirtiendo el metodo en un metodo de clase
    def verificar_Password(self,password_encriptada,password):#Se creara un metodo para realizar la verificacion de las password del usuario 
        #encriptado= generate_password_hash(password)#Esta variable recibira la password y la encriptara con el metodo generate_password_hash por eso se le pasa password
        print("Password encriptada desde funcion verificar password usuario.py", password_encriptada, password)
        coincide=check_password_hash(password_encriptada,password)#Validara que la password sea igual que la del texto que recibio por eso se le pasa la variable encriptado y el valor que tiene password para ver si coinciden
        return coincide