from app.models.entities.grupos import Grupos
from flask import flash, render_template
from app.database.db import get_connection

class ModeloGrupos:
    @classmethod
    def crear_grupos(self, equipo, grupo):
        try:
            connection= get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre FROM grupos WHERE nombre = %s ", (grupo,))
                data = cursor.fetchone()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
                #fectchone es para verificar si almenos una linea completa de la tabla coincide y fetchall busca coincidencias en todas las lineas de la tabla
                idgrupo=data[0]
                print(idgrupo)
                cursor.execute("UPDATE `equipos` SET `grupo_id` = %s  WHERE `equipos`.`nombre_equipo` = %s ", (idgrupo, equipo,))
                connection.commit()
                return True
        except Exception as e:
            print(e)
            flash("No se pudo agregar el equipo al grupo")
