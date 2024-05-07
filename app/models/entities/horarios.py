class Horarios:
    def __init__(self, id, id_equipo, dia, hora_inicio, hora_fin):
        self.id = id
        self.id_equipo = id_equipo
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def __str__(self):
        return f"Horarios(id={self.id}, id_equipo={self.id_equipo}, dia={self.dia}, hora_inicio={self.hora_inicio},hora_fin={self.hora_fin})"

    def get_id(self):
        return str(self.id)