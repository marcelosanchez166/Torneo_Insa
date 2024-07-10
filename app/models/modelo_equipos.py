from app.models.entities.equipos import Equipos
from flask import flash, render_template
from app.database.db import get_connection
from app.models.modelo_horarios import Modelo_horarios

class ModeloEquipos:
    @classmethod
    def add_teams(self, horas_por_dia, Add_Equipos):
        print(type(horas_por_dia), "Desde addteams")
        print("Desde metodo addteams de ModeloEquipos", Add_Equipos.nombre_equipo, Add_Equipos.representante, Add_Equipos.subrepresentante, Add_Equipos.correo)
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo FROM equipos WHERE nombre_equipo = %s OR correo = %s", (Add_Equipos.nombre_equipo, Add_Equipos.correo,))
                data = cursor.fetchone()
                print(data)
                if data is None:  # si no hay registros en la tabla devuelve None
                    sql = """INSERT INTO equipos (nombre_equipo, representante, subrepresentante, correo) VALUES (%s, %s, %s, %s)"""
                    cursor.execute(sql, (Add_Equipos.nombre_equipo, Add_Equipos.representante, Add_Equipos.subrepresentante, Add_Equipos.correo))
                    connection.commit()
                    # Obtener el ID del equipo recién insertado
                    cursor.execute("SELECT id FROM equipos WHERE nombre_equipo = %s", (Add_Equipos.nombre_equipo,))
                    data3 = cursor.fetchone()
                    if data3:
                        team_id = data3[0]
                        add_horarios = Modelo_horarios.agregar_horarios(horas_por_dia, team_id)
                        return True
                    else:
                        flash("Error retrieving the newly inserted team's ID", "warning")
                        return None
                else:
                    flash("The team already exists", "warning")
                    return render_template("Equipos.html")
        except Exception as ex:
            print(f"Error durante la inserción de equipos: {ex}")
            flash('Error adding the team to the database', 'warning')
            return None



    @classmethod
    def update_equipos(self, update, horas_por_dia):
        connection = get_connection()
        try:
            print(update.representante, update.id,"Este es el nuevo estado que se le dara si se le da click al boton done")
            print(horas_por_dia, "Dede el metodo update equipos")
            '''Marcar como realizada'''
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos WHERE id = %s ", (update.id,))
                data = cursor.fetchone()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
                #fectchone es para verificar si almenos una linea completa de la tabla coincide y fetchall busca coincidencias en todas las lineas de la tabla
            print(data, "Imprimiendo la variable result ")
            if data is not None:
                    with connection.cursor() as cursor:
                        #UPDATE `equipos` SET `nombre_equipo` = 'Barcelona ', `representante` = 'Marcelo Sanchez', `subrepresentante` = 'Gloria Vasquez', `correo` = 'marcelosanchez1506@gmail.com' WHERE `equipos`.`id` = 93;
                        cursor.execute("UPDATE `equipos` SET `nombre_equipo` = %s, `representante` = %s, `subrepresentante` = %s, `correo` = %s WHERE `equipos`.`id` = %s ", (update.nombre_equipo, update.representante, update.subrepresentante, update.correo, data[0],))
                        Updated = cursor.fetchone()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
                        #fectchone es para verificar si almenos una linea completa de la tabla coincide y fetchall busca coincidencias en todas las lineas de la tabla
                        # Obtener el ID del equipo recién insertado
                        connection.commit()
                        updating_team = Equipos(id = update.id , nombre_equipo=update.nombre_equipo, representante=update.representante, subrepresentante=update.subrepresentante, correo=update.correo, grupo_id=update.grupo_id)
                        print(updating_team, "Imprimiendo lo que se le envia a la clase Usuario desde cuando se le envian las cosas despues de hacer el update del equipo")
                        if data:
                            team_id = data[0]
                            print(team_id)
                            add_horarios = Modelo_horarios.actualizar_horarios(horas_por_dia, team_id)
                            print(add_horarios)
                            return True
                        else:
                            flash("Error retrieving the newly inserted team's ID", "warning")
                            return None
                    # updating_team = Equipos(id = update.id , nombre_equipo=update.nombre_equipo, representante=update.representante, subrepresentante=update.subrepresentante, correo=update.correo, grupo_id=update.grupo_id)
                    # print(updating_team, "Imprimiendo lo que se le envia a la clase Usuario desde cuando se le envian las cosas despues de hacer el update del equipo")
                    # return Updated, updating_team
            else:
                    flash('Fallo actualizando datos del equipo', 'warning')
                    return render_template("Equipos.html")
        except  Exception as ex:
            print(f"Error durante la actualizacion: {ex}")
            flash('This update has already been completed','warning')
            raise Exception(str(ex))


    @classmethod
    def delete_equipos(self, delete_equipo):
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos WHERE id = %s ", (delete_equipo.id,))
            data = cursor.fetchone()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
            #fectchone es para verificar si almenos una linea completa de la tabla coincide y fetchall busca coincidencias en todas las lineas de la tabla
            print(data, "Imprimiendo la variable result ")
            if data is not None:
                with connection.cursor() as cursor:

                    # Eliminar los horarios asociados primero
                    cursor.execute("DELETE FROM horarios WHERE id_equipo = %s", (delete_equipo.id,))
                    connection.commit()
                    
                    # Ahora eliminar el equipo
                    cursor.execute("DELETE FROM equipos WHERE id = %s", (delete_equipo.id,))
                    connection.commit()

                    # cursor.execute("DELETE FROM equipos WHERE id = %s ", (delete_equipo.id,))
                    # connection.commit()
                deleting_team = Equipos(id = delete_equipo.id , nombre_equipo=delete_equipo.nombre_equipo, representante=delete_equipo.representante, subrepresentante=delete_equipo.subrepresentante, correo=delete_equipo.correo, grupo_id=delete_equipo.grupo_id)
                print(deleting_team, "Imprimiendo lo que se le envia a la clase Equipos desde cuando se le envian las cosas despues de hacer el update del equipo")
                return  deleting_team
            else:
                flash('Fallo actualizando datos del equipo', 'warning')
                return render_template("Equipos.html")