class Equipos:
    def __init__(self, id, nombre_equipo, representante, subrepresentante, correo, grupo_id):
        self.id= id
        self.nombre_equipo = nombre_equipo
        self.representante = representante
        self.subrepresentante = subrepresentante
        self.correo = correo
        self.grupo_id = grupo_id

    def __str__(self):
        return f"Equipos(id={self.id}, nombre_equipo={self.nombre_equipo}, representante={self.representante}, subrepresentante={self.subrepresentante},correo={self.correo}, grupo_id={self.grupo_id})"


    def get_id(self):
        return str(self.id)