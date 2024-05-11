from flask import flash, render_template
from app.database.db import get_connection
from app.models.entities.horarios import Horarios

class Modelo_horarios:
    @classmethod
    def agregar_horarios(self,horas_por_dia, id_equipo):
        print(horas_por_dia, "Horarios desde el metodo agregar horarios clase Modelo horarios")
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                # cursor.execute("SELECT id, id_equipo, dia, hora_inicio, hora_fin,  FROM horarios WHERE id_equipo = %s ", (id_equipo,))
                # data = cursor.fetchone()
                # if data is not None:
                for dia, horas in horas_por_dia.items():
                    sql= """INSERT INTO `horarios` (`id_equipo`, `dia`, `hora_inicio`, `hora_fin`)  VALUES (%s,%s,%s,%s)"""
                    cursor.execute(sql, (id_equipo, dia, horas['inicio'], horas['fin']))
                    print(dia, horas, "Valores recorridos desde el for desde la clase Modelo_horarios")
                    # cursor.execute(sql,(horas_por_dia.id_equipo, horas_por_dia.dia, horas_por_dia.hora_inicio, horas_por_dia.hora_fin))
                    connection.commit()
                    # add_horarios = Horarios(id = horas_por_dia.id , id_equipo=horas_por_dia.id_equipo, dia=horas_por_dia.dia, hora_inicio=horas_por_dia.hora_inicio, correo=horas_por_dia.hora_fin)
                    # print(add_horarios, "Imprimiendo lo que se le envia a la clase Usuario desde cuando se le envian las cosas despues de hacer el update del equipo")
                    # return add_horarios
                    return True
                # else:
                #     flash('Fallo actualizando datos del equipo', 'warning')
                #     return render_template("Equipos.html")
        except Exception as ex:
            print(f"Error durante la inserción de los horarios a la tabla horarios: {ex}")
            return flash('Error agregando el equipo a la base de datos', 'warning')