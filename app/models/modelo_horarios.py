from flask import flash
from app.database.db import get_connection

from flask import flash
from app.database.db import get_connection

class Modelo_horarios:
    @classmethod
    def agregar_horarios(cls, horas_por_dia, team_id):
        print(horas_por_dia, team_id, "Horarios desde el metodo agregar horarios clase Modelo horarios")
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                # Comprobar si horas_por_dia es un diccionario
                if isinstance(horas_por_dia, dict):
                    for dia, horas in horas_por_dia.items():
                        sql = """INSERT INTO horarios (id_equipo, dia, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s)"""
                        cursor.execute(sql, (team_id, dia, horas['inicio'], horas['fin']))
                        connection.commit()
                        print(dia, horas, "Valores recorridos desde el for desde la clase Modelo_horarios")
                else:
                    for horario in horas_por_dia:
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
        print(type)
        print(horas_por_dia, team_id, "Horarios desde el metodo Actualizar horarios clase Modelo horarios")
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                for horario in horas_por_dia:
                    sql = """UPDATE `horarios` SET `dia` = %s, `hora_inicio` = %s, `hora_fin` = %s WHERE `id_equipo` = %s"""
                    cursor.execute(sql, (horario['dia'], horario['hora_inicio'], horario['hora_fin'], team_id))
                    print(horario['dia'], horario, "Valores recorridos desde el for desde la clase Modelo_horarios")
                connection.commit()
            return True
        except Exception as ex:
            print(f"Error durante la actualizacion de los horarios metodo actualizar horarios a la tabla horarios: {ex}")
            flash('Error adding schedules to the database', 'warning')
            return None
