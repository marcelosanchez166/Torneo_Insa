from flask import flash
from app.database.db import get_connection
from app.models.entities.horarios import Horarios
from flask import render_template


class Modelo_partidos:
    @classmethod
    def agregar_partido(self, ):
        try:
            connection= get_connection()
            with connection.cursor() as cursor:
                sql = """INSERT INTO partidos (id_equipo_local, id_equipo_visitante, resultado, datetime, grupo_id) VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (self.id_equipo_local, self.id_equipo_visitante, self.datetime, self.gruo_id))
                connection.commit()
                return True
        except Exception as e:
            print(e)
            flash("No se pudo agregar el partido")
            return False

