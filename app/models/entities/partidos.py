class Partidos:
    def __init__(self, id, id_equipo_local,id_equipo_visitante, resultado ,date, grupo_id):
        self.id = id
        self.id_equipo_local = id_equipo_local
        self.id_equipo_visitante = id_equipo_visitante
        self.resultado = resultado
        self.grupo_id = grupo_id
        self.date = date


    def __str__(self):
        return f"Horarios(id={self.id}, id_equipo_local={self.id_equipo_local}, id_equipo_visitante={self.id_equipo_visitante}, resultado={self.resultado},date={self.date}, grupo_id={self.grupo_id})"

    def get_id(self):
        return str(self.id)