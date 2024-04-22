from app.models.entities.equipos import Equipos
#from app import current_user
from flask import flash, render_template, redirect, url_for, flash
from app.database.db import get_connection


class ModeloEquipos():
    @classmethod
    def add_teams(self, Add_teams):
        print("Desde metodo addteams de ModeloEquipos",Add_teams.nombre_equipo)
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos WHERE nombre_equipo = %s AND correo = %s""",(Add_teams.nombre_equipo,Add_teams.correo))
                data = cursor.fetchone()
                print(data[1])
                if not data:  # si no hay registros en la tabla devuelve None
                    cursor.execute("INSERT INTO (nombre_equipo, representante, subrepresentante, correo) VALUES  VALUES(%s,%s,%s,%s)",(Add_teams.nombre_equipo,Add_teams.representante, Add_teams.subrepresentante, Add_teams.correo))
                    agregar_equipo = Equipos(id = None , nombre_equipo=Add_teams.nombre_equipo, representante=Add_teams.representante, subrepresentante=Add_teams.subrepresentante, correo= Add_teams.correo )
                    return agregar_equipo
                else:
                    flash("The task exist","warning")
                    return render_template("Equipos.html")
        except Exception as ex:
            print(f"Error durante la inserción: {ex}")
            return flash('Error agregando el equipo a la base de datos', 'warning')
