from flask import flash
from app.database.db import get_connection

class Modelo_horarios:
    @classmethod
    def agregar_horarios(self,id_equipo, horarios):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, id_equipo, dia, hora_inicio, hora_fin,  FROM horarios WHERE id_equipo = %s ", (id_equipo,))
                data = cursor.fetchone()
                if data is not None:
                    sql= """INSERT INTO `horarios` (`id_equipo`, `dia`, `hora_inicio`, `hora_fin`)  VALUES (%s,%s,%s,%s)"""
                    cursor.execute(sql,(horarios.id_equipo, horarios.dia, horarios.hora_inicio, horarios.hora_fin))
                    connection.commit()
        except Exception as ex:
            print(f"Error durante la inserción: {ex}")
            return flash('Error agregando el equipo a la base de datos', 'warning')