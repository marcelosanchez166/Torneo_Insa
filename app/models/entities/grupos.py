class Grupos:
    def __init__(self, id, nombre):
        self.id= id
        self.nombre_equipo = nombre

    def __str__(self):
        return f"Grupos(id={self.id}, nombre={self.nombre})"

    def get_id(self):
        return str(self.id)