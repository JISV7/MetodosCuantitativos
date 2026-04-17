import numpy as np
from scipy.optimize import linear_sum_assignment, linprog

class MetodoHungaro:
    """
    Resuelve el problema de asignación Programador-Tarea usando el Método Húngaro.
    """
    def __init__(self, programadores, tareas):
        self.programadores = programadores
        self.tareas = tareas
        # Un valor muy alto para representar una asignación imposible
        self.costo_infinito = 1e9 
        self.matriz_costos = self._crear_matriz_costos()

    def _crear_matriz_costos(self):
        """
        Crea la matriz de costos. El costo es el de contratación del programador.
        Si un programador no tiene la habilidad para una tarea, el costo es infinito.
        """
        num_programadores = len(self.programadores)
        num_tareas = len(self.tareas)
        matriz = np.full((num_programadores, num_tareas), self.costo_infinito)

        for i, prog in enumerate(self.programadores):
            for j, tarea in enumerate(self.tareas):
                # Asigna el costo solo si el programador tiene la habilidad y está disponible
                if tarea.habilidad_requerida in prog.habilidades and prog.disponibilidad:
                    matriz[i, j] = prog.costo_contratacion
        return matriz

    def resolver(self):
        """
        Ejecuta el algoritmo de asignación.
        Retorna las asignaciones, el costo total y los programadores asignados.
        """
        if self.matriz_costos.size == 0:
            return [], 0, []

        filas_ind, cols_ind = linear_sum_assignment(self.matriz_costos)

        asignaciones = []
        programadores_asignados = []
        costo_total = 0

        for i, j in zip(filas_ind, cols_ind):
            costo = self.matriz_costos[i, j]
            if costo < self.costo_infinito:
                programador = self.programadores[i]
                tarea = self.tareas[j]
                asignaciones.append((programador, tarea, costo))
                programadores_asignados.append(programador)
                costo_total += costo

        return asignaciones, costo_total, programadores_asignados

class ProblemaTransporte:
    """
    Resuelve el problema de distribución de programadores a sedes.
    """
    def __init__(self, programadores, sedes, costos_traslado):
        self.oferta = np.array([1] * len(programadores)) # Cada programador es una oferta
        self.demanda = np.array([s.programadores_requeridos for s in sedes])
        self.matriz_costos_traslado = np.array(costos_traslado)
        self.programadores = programadores
        self.sedes = sedes

    def resolver(self):
        """
        Resuelve el problema de transporte usando programación lineal.
        Retorna la distribución, el costo total de traslado y un mensaje de estado.
        """
        # Aplanar la matriz de costos para el solver de programación lineal
        c = self.matriz_costos_traslado.flatten()

        # Crear matriz de restricciones de igualdad para la oferta y la demanda
        num_oferta, num_demanda = self.matriz_costos_traslado.shape
        
        A_eq = []
        # Restricciones de oferta (cada programador se asigna una vez)
        for i in range(num_oferta):
            fila = np.zeros(num_oferta * num_demanda)
            fila[i * num_demanda : (i + 1) * num_demanda] = 1
            A_eq.append(fila)

        # Restricciones de demanda (cada sede recibe los programadores que necesita)
        for j in range(num_demanda):
            fila = np.zeros(num_oferta * num_demanda)
            fila[j::num_demanda] = 1
            A_eq.append(fila)
        
        A_eq = np.array(A_eq)
        b_eq = np.concatenate([self.oferta, self.demanda])
        
        # Límites para las variables de decisión (la asignación es 0 o 1)
        bounds = [(0, 1) for _ in range(len(c))]

        resultado = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        if not resultado.success:
            return None, 0, f"No se encontró solución óptima: {resultado.message}"

        distribucion_flat = resultado.x
        distribucion_matrix = distribucion_flat.reshape((num_oferta, num_demanda))
        
        distribucion_final = []
        costo_total_traslado = resultado.fun

        for i in range(num_oferta):
            for j in range(num_demanda):
                if distribucion_matrix[i, j] > 0.5: # Si la asignación es cercana a 1
                    distribucion_final.append((self.programadores[i], self.sedes[j], self.matriz_costos_traslado[i, j]))

        return distribucion_final, costo_total_traslado, "Solución óptima encontrada."