from app.models.entities.equipos import Equipos
#from app import current_user
from flask import flash, render_template, redirect, url_for, flash
from app.database.db import get_connection


class ModeloEquipos():
    @classmethod
    def add_teams(self, Add_Equipos):
        print("Desde metodo addteams de ModeloEquipos",Add_Equipos.nombre_equipo,Add_Equipos.representante,Add_Equipos.subrepresentante,  Add_Equipos.correo )
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre_equipo, representante, subrepresentante, correo, grupo_id FROM equipos WHERE nombre_equipo = %s AND correo = %s", (Add_Equipos.nombre_equipo,Add_Equipos.correo,))
                data = cursor.fetchone()#fetchone() devuelve una sola fila (la primera fila que cumple con la condición) o None si no hay ninguna fila que coincida.
                #fectchone es para verificar si almenos una linea completa de la tabla coincide y fetchall busca coincidencias en todas las lineas de la tabla
                #print("Imprimiendo data que se obtiene de la base de datos con el select",data[1], data[4])
                if  data is None or data == None:  # si no hay registros en la tabla devuelve None
                    sql= """INSERT INTO equipos (nombre_equipo, representante, subrepresentante, correo)  VALUES (%s,%s,%s,%s)"""
                    cursor.execute(sql,(Add_Equipos.nombre_equipo,Add_Equipos.representante, Add_Equipos.subrepresentante, Add_Equipos.correo))
                    connection.commit()
                    agregar_equipo = Equipos(id = None , nombre_equipo=Add_Equipos.nombre_equipo, representante=Add_Equipos.representante, subrepresentante=Add_Equipos.subrepresentante, correo= Add_Equipos.correo, grupo_id= None )
                    print(agregar_equipo, "Imprimiendo lo que se le envia a la clase Equipos desde el metodo de clase add_teams cuando se le envian las cosas despues de hacer el insert")
                    return agregar_equipo
                else:
                    flash("The team exist","warning")
                    return render_template("Equipos.html")
        except Exception as ex:
            print(f"Error durante la inserción: {ex}")
            return flash('Error agregando el equipo a la base de datos', 'warning')
