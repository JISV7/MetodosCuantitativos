import numpy as np
from scipy.optimize import linear_sum_assignment

def ingresar_matriz_costos():
    """
    Permite al usuario ingresar los datos para crear la matriz de costos dinámicamente.
    """
    print("--- Creación de la Matriz de Costos ---")

    # Asegurar que se ingresen números válidos para las dimensiones
    while True:
        try:
            num_programadores = int(input("Ingrese el número de programadores (filas): "))
            num_tareas = int(input("Ingrese el número de tareas (columnas): "))
            if num_programadores <= 0 or num_tareas <= 0:
                print("Error: El número debe ser un entero positivo. Intente de nuevo.")
                continue
            break
        except ValueError:
            print("Error: Por favor, ingrese un número entero válido.")

    matriz = []
    print("\nAhora, ingrese los costos de asignación para cada celda:")

    # Bucles anidados para solicitar cada costo
    for i in range(num_programadores):
        fila_actual = []
        print(f"\n--- Costos para el Programador {i + 1} ---")
        for j in range(num_tareas):
            # Bucle para asegurar que cada costo sea un número válido
            while True:
                try:
                    costo_str = input(f"  Costo para la Tarea {j + 1}: ")
                    costo = float(costo_str)
                    fila_actual.append(costo)
                    break # Sale del bucle de validación si el número es correcto
                except ValueError:
                    print("Error: Ingrese un número válido para el costo.")
        matriz.append(fila_actual)

    # Convierte la lista de listas de Python a una matriz de NumPy
    return np.array(matriz)

# --- EJECUCIÓN PRINCIPAL DEL SCRIPT ---

# 1. Obtener la matriz de costos directamente del usuario
matriz_costos = ingresar_matriz_costos()

# 2. Resolver el problema de asignación solo si la matriz no está vacía
if matriz_costos.size > 0:
    # La función de SciPy maneja eficientemente la asignación
    filas_opt, cols_opt = linear_sum_assignment(matriz_costos)

    # 3. Mostrar los resultados
    print("\n" + "="*50)
    print("--- Matriz de Costos Ingresada ---")
    print(matriz_costos)
    print("\n" + "="*50 + "\n")

    print("--- Asignación Óptima ---")

    # Sumar los costos de las asignaciones óptimas
    costo_total = matriz_costos[filas_opt, cols_opt].sum()

    # Mostrar cada asignación individual
    for fila, columna in zip(filas_opt, cols_opt):
        costo = matriz_costos[fila, columna]
        print(f"Programador {fila + 1} --> Tarea {columna + 1} (Costo: {costo})")

    print("\n" + "="*50 + "\n")
    print(f"Costo Total Mínimo de Contratación: {costo_total}")
else:
    print("\nNo se ingresaron datos. El programa ha finalizado.")