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


#Arreglar la actualizacion ya que actualmente no estoy usando los datos que recibo del formulario por ende daria error porque estaria usando el mismo grupo_id
    @classmethod
    def update_grupo(self, id_equipo,  equipo, grupo):
        print(id_equipo, grupo, "Este es el ID del Equipo que servira para actualizar el grupo al que pertence el equipo")
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT equipos.nombre_equipo, grupos.nombre, grupos.id FROM equipos INNER JOIN grupos ON equipos.grupo_id = grupos.id WHERE equipos.id = %s", (id_equipo,))
                data = cursor.fetchone()
                cursor.execute("SELECT id FROM grupos WHERE nombre = %s ", (grupo,))
                data_grupo = cursor.fetchone()
                data_grupo=data_grupo[0]
                if data is not None:
                    cursor.execute("UPDATE equipos SET grupo_id = %s WHERE id = %s ",(data_grupo, id_equipo, ))
                    connection.commit()
                    flash("Grupo actualizado para el equipo exitosamente", "success")
                    return True
                else:
                    flash("Fallo en la actualizacion del grupo para el equipo", "warning")
                    return False
        except Exception as e:
            print(e, "Error actualizando grupo")
            flash("Fallo en la actualizacion del grupo para el equipo", "warning")
            return False


    @classmethod
    def delete_grupos(self, id_equipo):
        print(id_equipo, "Este es el ID del Equipo que servira para validar y luego hacer el update a null para el grupo_id")
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos WHERE id = %s ", (id_equipo,))
                data = cursor.fetchone()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
                #fectchone es para verificar si almenos una linea completa de la tabla coincide y fetchall busca coincidencias en todas las lineas de la tabla
                print(data, "Imprimiendo la variable result ")
                if data is not None:
                    with connection.cursor() as cursor:
                        cursor.execute("UPDATE `equipos` SET `grupo_id` = %s WHERE `equipos`.`id` = %s", (None, id_equipo,))
                        connection.commit()
                        flash("Equipo eliminado del grupo", "success")
                        return True
                else:
                    flash('Fallo actualizando datos del equipo', 'warning')
                    return render_template("Equipos.html")
                return True
        except Exception as e:
            print(e)
            flash("No se pudo eliminar el equipo del grupo")
            return False