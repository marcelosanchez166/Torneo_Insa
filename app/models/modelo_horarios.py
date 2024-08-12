from flask import flash
from app.database.db import get_connection
from app.models.entities.horarios import Horarios
from flask import render_template


class Modelo_horarios:
    @classmethod
    def agregar_horarios(self, horas_por_dia, team_id):
        print(horas_por_dia, team_id, "Horarios desde el metodo agregar horarios clase Modelo horarios")
        connection = get_connection()
        print(isinstance(horas_por_dia, dict))
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, id_equipo, dia, hora_inicio, hora_fin FROM horarios WHERE id_equipo = %s", (team_id,))
                horarios_dia = cursor.fetchall()

                horarios = []
                dias_existentes = []
                if horarios_dia is not None:
                    for row in horarios_dia:
                        horario = {
                            'id': row[0],
                            'id_equipo': row[1],
                            'dia': row[2],
                            'hora_inicio': row[3],
                            'hora_fin': row[4]
                        }
                        horarios.append(horario)
                        dias_existentes.append(horario['dia'])
                    print(dias_existentes)
                else:
                    print("No se encontraron horarios existentes para el equipo.")

                # Comprobar si horas_por_dia es un diccionario
                if isinstance(horas_por_dia, dict):
                    for dia, horas in horas_por_dia.items():
                        if dia in dias_existentes:
                            flash("El Dia que desea agregar a los horarios del equipo seleccionado ya existe ", 'warning')
                            print("Error ingresando el horario porque el dia ya existe para el equipo")
                        else:
                            sql = """INSERT INTO horarios (id_equipo, dia, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s)"""
                            cursor.execute(sql, (team_id, dia, horas['inicio'], horas['fin']))
                            connection.commit()
                            print(dia, horas, "Valores recorridos desde el for desde la clase Modelo_horarios")
                else:
                    for horario in horas_por_dia:
                        if horario['dia'] in dias_existentes:
                            flash("El Dia que desea agregar a los horarios del equipo seleccionado ya existe ", 'warning')
                        else:
                            sql = """INSERT INTO horarios (id_equipo, dia, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s)"""
                            cursor.execute(sql, (team_id, horario['dia'], horario['hora_inicio'], horario['hora_fin']))
                            print(horario['dia'], horario, "Valores recorridos desde el for desde la clase Modelo_horarios")
                            connection.commit()
            return True
        except Exception as ex:
            print(f"Error durante la inserción o actualizacion de los horarios a la tabla horarios: {ex}")
            flash('Error adding schedules to the database', 'warning')
            return None



    @classmethod
    def actualizar_horarios(cls, horas_por_dia, team_id):
        print(len(horas_por_dia), team_id, "Horarios desde el metodo Actualizar horarios clase Modelo horarios y el tamano de horas_por_dia")
        connection = get_connection()
        try:
            # Primero obtenemos los IDs de los horarios correspondientes al equipo
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM horarios WHERE id_equipo = %s", (team_id,))
                horarios_ids = cursor.fetchall()  # Use fetchall para obtener todas las filas que coincidan, esto devuelve una lista de tuplas, 
                #y el fetchone devuelve la primera linea que coincida osea un tupla nada mas
            
            print(type(horarios_ids), horarios_ids, "Imprimiendo el tipo de horarios_ids cuando hago el select y lo obtengo con el fetchall() ")
            # Asegurarse de que se han obtenido los IDs
            if not horarios_ids:
                print("No se encontraron horarios para el equipo proporcionado.")
                return None

            # Convertir la lista de tuplas en una lista de IDs de manera más explícita
            id_list = []
            for id_tuple in horarios_ids:
                id_list.append(id_tuple[0])
                print(id_list, "Lista de IDs de horarios desde la clase Modelo_horarios")

            # Verificamos si el número de horarios obtenidos coincide con el número de horarios proporcionados
            if len(id_list) != len(horas_por_dia):
                print("El número de horarios obtenidos no coincide con el número de horarios proporcionados.")
                return None

            # Actualizamos cada horario usando su id
            with connection.cursor() as cursor:
                for idx, horario in enumerate(horas_por_dia):
                    sql = """UPDATE horarios SET dia = %s, hora_inicio = %s, hora_fin = %s WHERE id = %s AND id_equipo = %s"""
                    cursor.execute(sql, (horario['dia'], horario['hora_inicio'], horario['hora_fin'], id_list[idx], team_id))
                    print(horario['dia'], horario, id_list[idx], "Valores recorridos desde el for desde la clase Modelo_horarios")
                connection.commit()
            return True
        except Exception as ex:
            print(f"Error durante la actualización de los horarios método actualizar horarios a la tabla horarios: {ex}")
            flash('Error adding schedules to the database', 'warning')
            return None


    @classmethod
    def delete_horarios(self, delete_horario):
        connection = get_connection()
        print(delete_horario.id, "Este es el id que se va a eliminar de los horarios")
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, id_equipo, dia, hora_inicio, hora_fin  FROM horarios WHERE id = %s ", (delete_horario.id,))
            data = cursor.fetchone()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
            #fectchone es para verificar si almenos una linea completa de la tabla coincide y fetchall busca coincidencias en todas las lineas de la tabla
            print(data, "Imprimiendo la variable result ")
            if data is not None:
                with connection.cursor() as cursor:
                    # Eliminar los horarios asociados primero
                    cursor.execute("DELETE FROM horarios WHERE id = %s", (delete_horario.id,))
                    connection.commit()

                deleting_team = Horarios(id = delete_horario.id , id_equipo=delete_horario.id_equipo, dia=delete_horario.dia, hora_inicio=delete_horario.hora_inicio, hora_fin=delete_horario.hora_fin)
                print(deleting_team)
                return  deleting_team
            else:
                flash('Fallo eliminando datos del horario', 'warning')
                return render_template("horarios.html")