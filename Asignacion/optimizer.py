import numpy as np
from scipy.optimize import linear_sum_assignment, linprog

class Optimizador:
    """
    Clase que encapsula los algoritmos de optimización.
    """
    @staticmethod
    def metodo_hungaro(matriz_costos):
        """
        Resuelve el problema de asignación usando el Método Húngaro.
        Args:
            matriz_costos (np.array): La matriz de costos.
        Returns:
            tuple: Índices de filas, índices de columnas y costo total.
        """
        if matriz_costos.size == 0:
            return None, None, 0

        filas_opt, cols_opt = linear_sum_assignment(matriz_costos)
        costo_total = matriz_costos[filas_opt, cols_opt].sum()
        
        return filas_opt, cols_opt, costo_total

    @staticmethod
    def problema_transporte(costos_transporte, oferta, demanda):
        """
        Resuelve el problema de transporte utilizando programación lineal.
        Args:
            costos_transporte (np.array): Matriz de costos (origen x destino).
            oferta (list): Lista con la cantidad de oferta en cada origen.
            demanda (list): Lista con la cantidad de demanda en cada destino.
        Returns:
            dict: Un diccionario con los resultados ('flujo', 'costo', 'mensaje', 'exito').
        """
        num_origenes, num_destinos = costos_transporte.shape

        # Validación básica: La oferta total debe ser al menos igual a la demanda total.
        if sum(oferta) < sum(demanda):
            return {
                "flujo": None,
                "costo": None,
                "mensaje": "Error: La oferta total es menor que la demanda total. No es posible satisfacer los requerimientos.",
                "exito": False
            }

        # 1. Vector de costos (c): Aplanamos la matriz de costos a un solo vector.
        c = costos_transporte.flatten()

        # 2. Matriz de restricciones de igualdad (A_eq) y vector de resultados (b_eq)
        # Tendremos una restricción por cada origen y cada destino.
        A_eq = []
        
        # Restricciones de oferta: la suma de lo que sale de un origen debe ser <= a su oferta.
        # (Usaremos igualdad, el solver puede manejar un "slack" o excedente si la oferta > demanda)
        for i in range(num_origenes):
            fila = np.zeros(num_origenes * num_destinos)
            fila[i * num_destinos : (i + 1) * num_destinos] = 1
            A_eq.append(fila)

        # Restricciones de demanda: la suma de lo que llega a un destino debe ser == a su demanda.
        for j in range(num_destinos):
            fila = np.zeros(num_origenes * num_destinos)
            for i in range(num_origenes):
                fila[i * num_destinos + j] = 1
            A_eq.append(fila)
        
        A_eq = np.array(A_eq)
        
        # El vector b_eq contiene los valores de oferta y demanda correspondientes
        b_eq = np.concatenate([oferta, demanda])

        # 3. Límites de las variables (bounds): no se puede transportar una cantidad negativa.
        bounds = [(0, None) for _ in range(len(c))]

        # 4. Resolver el problema de programación lineal
        resultado = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        # 5. Procesar y devolver el resultado
        if resultado.success:
            flujo_optimo = resultado.x.reshape((num_origenes, num_destinos))
            costo_total = resultado.fun
            return {
                "flujo": flujo_optimo,
                "costo": costo_total,
                "mensaje": "Solución óptima encontrada.",
                "exito": True
            }
        else:
            return {
                "flujo": None,
                "costo": None,
                "mensaje": f"No se pudo encontrar una solución. Estado: {resultado.message}",
                "exito": False
            }