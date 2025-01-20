from flask import flash
from app.database.db import get_connection
from app.models.entities.horarios import Horarios
from flask import render_template
from datetime import datetime


class Modelo_partidos:
    @classmethod
    def agregar_partido(self, Egrupos):
        print(Egrupos.id_equipo_local, Egrupos.id_equipo_visitante,
            Egrupos.date, Egrupos.grupo_id, "DEsde Modelo Partidos clase")
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                # formateando la fecha al formato de la fecha de la base de datos
                Egrupos.date = datetime.strptime(
                    Egrupos.date, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
                # Guardar el partido en la base de datos
                sql = """INSERT INTO partidos (id_equipo_local, id_equipo_visitante, datetime, grupo_id) VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql, (Egrupos.id_equipo_local,
                            Egrupos.id_equipo_visitante, Egrupos.date, Egrupos.grupo_id))
                connection.commit()
                flash("Partido agregado al grupo exitosamente", "success")
                return True
        except Exception as e:
            print(e, "No se pudo agregar el partido desde Modelo Partidos ")
            flash("No se pudo agregar el partido")
            return False
