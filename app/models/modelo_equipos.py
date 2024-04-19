from app.models.entities.equipos import Equipos
#from app import current_user
from flask import flash, render_template, redirect, url_for, flash
from app.database.db import get_connection


class ModeloEquipos():
    @classmethod
    def add_teams(self, add_team):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM usuarios WHERE nombre_equipo = %s AND correo = %s""", 
                            (add_team.Nombre_Equipo,add_team.Email))
                data = cursor.fetchone()
                if data[1] != add_team.Nombre_Equipo:
                    cursor.execute("INSERT INTO (nombre_equipo, representante, subrepresentante, correo) VALUES  VALUES(%s,%s,%s,%s)",(add_team.Nombre_Equipo,add_team.Representante, add_team.SubRepresentante, add_team.Email))
                    agregar_equipo = Equipos(id = None , nombre_equipo=add_team.Nombre_Equipo, representante=add_team.Representante, subrepresentante=add_team.SubRepresentante, correo= add_team.Email )
        except Exception as ex:
            print(f"Error durante la inserción: {ex}")
            return flash('Error agregando el equipo a la base de datos', 'warning')
