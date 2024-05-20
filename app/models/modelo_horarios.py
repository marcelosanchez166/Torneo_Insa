from flask import flash
from app.database.db import get_connection

class Modelo_horarios:
    @classmethod
    def agregar_horarios(self, horas_por_dia, team_id):
        print(horas_por_dia, team_id, "Horarios desde el metodo agregar horarios clase Modelo horarios")
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                for dia, horas in horas_por_dia.items():
                    sql = """INSERT INTO horarios (id_equipo, dia, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s)"""
                    cursor.execute(sql, (team_id, dia, horas['inicio'], horas['fin']))
                    connection.commit()
                    print(dia, horas, "Valores recorridos desde el for desde la clase Modelo_horarios")
            return True
        except Exception as ex:
            print(f"Error durante la inserción de los horarios a la tabla horarios: {ex}")
            flash('Error adding schedules to the database', 'warning')
            return None
