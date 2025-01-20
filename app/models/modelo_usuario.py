# Este archivo servira para tener la logica del inicio de sesion
from app.models.entities.usuario import Usuario
# from app import db
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.db import get_connection


class ModeloUsuario():
    @classmethod
    def login(self, usuario):
        print(usuario.username, "usuarios enviados desde instancia de app", usuario.id)
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                print(cursor, "Imprimiendo el cursor")
                cursor.execute(
                    "SELECT id, username, password, email FROM usuarios WHERE username = %s", (usuario.username,))
                # Usamos el metodo fecthone porque solo esperamos recibir un registro en este caso solo el usuario
                data = cursor.fetchone()
                if data is not None:
                    print("password de data modelo usuario", data[2], data[0])
                    print("password desde modelo usuario", usuario.password)
                    if data != None:  # Verifica si hay datos y tiene al menos 3 elementos:
                        coincide = Usuario.verificar_Password(
                            data[2],  usuario.password)
                        if coincide:  # Si la variable coincide es verdadera
                            # usuario_logueado=Jugadores(data[0], None, None, None, None, None, None, data[1], data[2] )#Instanciamos la clase Usuario del archivo usuario.py y solo les pasamos los argumentos de las posiciones 0 y 1 que corresponden al id y al Nombre_usuario y la password y el tipo de usuario le ponemos None para no exponer esos campos
                            usuario_logueado = Usuario(
                                id=data[0], username=data[1],  password=data[2], email=data[3])
                            print(usuario_logueado)
                            return usuario_logueado
                        else:
                            flash("Please Check The Password", 'warning')
                    else:
                        flash("Verify your credencials", 'warning')
                else:
                    flash("User or Password Wron", "warning")
        except Exception as ex:
            raise Exception(ex)


# Este metodo sirve para que se pueda usar el id como inicio de sesion el id_jugador se recibe del metodo def load_user(id_jugador) que esta en el archivo app.py

    @classmethod
    def obtener_por_id(self, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                # En el format se le pasa el atributo que recibe el metodo obtener_por_id
                cursor.execute(
                    "SELECT id, username, password, email FROM usuarios WHERE id = %s", (id))
                # Usamos el metodo fecthone porque solo esperamos recibir un registro en este caso solo el id
                data = cursor.fetchone()
                # print("Imprimiendo la data de oobtener por ID ",data)
                if data is not None:
                    # Creamos una instancia de la clase Usuario y le pasamos las posiciones 0 que corresponde al id del usuario 1 de Nombre_usuario None para la clave ya que no la usaremos y la variable tipousuario que contiene las posiciones de 2 y 3 de la tupla data que son el id del tipo y el nombre del tipo
                    usuario_logueado = Usuario(
                        id=data[0], username=data[1], password=data[2], email=data[3])
                    # Este se almacena en la funcion load_user del archivo __init__.py
                    return usuario_logueado
                else:
                    # Puedes decidir qué hacer si no se encuentra un usuario con ese ID
                    return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def RegisterUser(self, usuario_re):
        print(usuario_re.username, "usuarios enviados desde instancia de app", usuario_re.password, usuario_re.email, "register usuario")
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, password, email FROM usuarios WHERE username = %s", (usuario_re.username,))
                data = cursor.fetchone()
                print(data, "Data desde el metodo RegisterUser")
                if data is None:   # Si el registro no existe en BD, lo crea
                    # Encriptar la contraseña antes de almacenarla
                    hashed_password = generate_password_hash(
                        usuario_re.password, method='pbkdf2:sha256')
                    # sql = """INSERT INTO usuarios (username, password, email) VALUES ('%s', '%s','%s');""" % \
                    #      (usuario_re.username, hashed_password, usuario_re.email)
                    sql = """INSERT INTO usuarios (username, password, email) VALUES (%s, %s, %s)"""
                    cursor.execute(sql, (usuario_re.username,hashed_password, usuario_re.email))
                    connection.commit()
                    # Obtener el ID generado automáticamente
                    new_user_id = cursor.lastrowid
                    print(
                        "data cuando hago el insert en el metodo registeruser \n", new_user_id)
                    register_user = Usuario(
                        id=new_user_id, username=usuario_re.username, password=hashed_password, email=usuario_re.email)
                    print(register_user, "Imprimiendo lo que se le envia a la clase Usuario desde cuando se le envian las cosas despues de hacer el insert")
                    return register_user
                else:
                    flash("User exist, Please choose another username", 'warning')
        except Exception as ex:
            print(f"Error durante la inserción: {ex}")
            raise Exception(str(ex))
