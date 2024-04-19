class Equipos:
    def __init__(self, id, nombre_equipo, representante, subrepresentante, correo, grupo_id):
        self.id= id
        self.nombre_equipo = nombre_equipo
        self.representante = representante
        self.subrepresentante = subrepresentante
        self.correo = correo
        self.grupo_id = grupo_id


    def get_id(self):
        return str(self.id)