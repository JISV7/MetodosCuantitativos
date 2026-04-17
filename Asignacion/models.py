class Programador:
    """Un programador con sus atributos."""
    def __init__(self, nombre, habilidades):
        self.nombre = nombre
        self.habilidades = habilidades

    def __str__(self):
        return f"Programador: {self.nombre} (Habilidades: {', '.join(self.habilidades)})"

class Tarea:
    """Una tarea con sus atributos."""
    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return f"Tarea: {self.nombre}"

class Sede:
    """Una sede o proyecto con sus atributos."""
    def __init__(self, nombre, localizacion, programadores_requeridos):
        self.nombre = nombre
        self.localizacion = localizacion
        self.programadores_requeridos = programadores_requeridos

    def __str__(self):
        return f"Sede: {self.nombre} ({self.localizacion}), Demanda: {self.programadores_requeridos} programadores"