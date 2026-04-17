class Programador:
    """Un programador con sus atributos principales."""
    def __init__(self, nombre, costo_contratacion, habilidades, disponibilidad=True):
        self.nombre = nombre
        self.costo_contratacion = costo_contratacion
        self.habilidades = habilidades
        self.disponibilidad = disponibilidad

    def __str__(self):
        return f"Programador: {self.nombre}, Costo: ${self.costo_contratacion}, Habilidades: {', '.join(self.habilidades)}"

class Tarea:
    """Una tarea con sus características y requisitos."""
    def __init__(self, nombre, complejidad, prioridad, plazo, habilidad_requerida):
        self.nombre = nombre
        self.complejidad = complejidad
        self.prioridad = prioridad
        self.plazo = plazo
        self.habilidad_requerida = habilidad_requerida

    def __str__(self):
        return f"Tarea: {self.nombre}, Habilidad Requerida: {self.habilidad_requerida}, Plazo: {self.plazo}"

class Sede:
    """Una sede o proyecto con su demanda de programadores."""
    def __init__(self, nombre, localizacion, programadores_requeridos):
        self.nombre = nombre
        self.localizacion = localizacion
        self.programadores_requeridos = programadores_requeridos

    def __str__(self):
        return f"Sede: {self.nombre}, Localización: {self.localizacion}, Demanda: {self.programadores_requeridos}"