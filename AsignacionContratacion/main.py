import os
import numpy as np
from modelos import Programador, Tarea, Sede
from optimizador import MetodoHungaro, ProblemaTransporte
from reporte import generar_reporte

# --- Datos de Ejemplo ---
programadores = [
    Programador("Ana", 1200, ["Python", "Java"]),
    Programador("Luis", 1100, ["JavaScript", "React"]),
    Programador("Carlos", 1350, ["Python", "Django"]),
    Programador("Maria", 1000, ["Java", "Spring"]),
    Programador("Pedro", 1500, ["Python", "AI/ML"]),
]

tareas = [
    Tarea("Desarrollo API", 8, 1, "4 semanas", "Python"),
    Tarea("Interfaz Frontend", 7, 2, "3 semanas", "React"),
    Tarea("Mantenimiento Base de Datos", 6, 3, "2 semanas", "Java"),
    Tarea("Modelo de Machine Learning", 9, 1, "6 semanas", "AI/ML"),
]

sedes = [
    Sede("Oficina Central", "Caracas", 2),
    Sede("Centro de Innovación", "Valencia", 2),
]

# Matriz de costos de traslado [Programador x Sede]
costos_traslado_ejemplo = [
#   Caracas, Valencia
    [100, 250], # Ana
    [120, 200], # Luis
    [150, 180], # Carlos
    [110, 210], # Maria
    [200, 150], # Pedro
]


def limpiar_consola():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_matriz(titulo, matriz, filas_nombres, cols_nombres):
    """Función para imprimir una matriz de forma legible."""
    print(f"\n--- {titulo} ---")
    # Imprimir encabezados de columnas
    encabezado = " " * 12
    for nombre in cols_nombres:
        encabezado += f"{nombre:<15}"
    print(encabezado)
    print("-" * len(encabezado))

    # Imprimir filas
    for i, nombre_fila in enumerate(filas_nombres):
        fila_str = f"{nombre_fila:<12}"
        for j in range(len(cols_nombres)):
            costo = matriz[i, j]
            fila_str += f"{str(int(costo) if costo < 1e8 else 'Inf'):<15}"
        print(fila_str)
    print("-" * len(encabezado))


def main():
    """Menú de la consola."""
    asignaciones_optimas = []
    costo_contratacion_total = 0
    programadores_contratados = []
    distribucion_optima = []
    costo_traslado_total = 0

    while True:
        limpiar_consola()
        print("===== SISTEMA DE ASIGNACIÓN Y CONTRATACIÓN DE PROGRAMADORES =====")
        print("\n1. Ver Datos Ingresados (Programadores, Tareas, Sedes)")
        print("2. Ejecutar Asignación Óptima de Tareas (Método Húngaro)")
        print("3. Ejecutar Distribución a Sedes (Problema de Transporte)")
        print("4. Generar Reporte Final")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            print("--- Programadores Disponibles ---")
            for p in programadores: print(p)
            print("\n--- Tareas Pendientes ---")
            for t in tareas: print(t)
            print("\n--- Sedes con Demanda ---")
            for s in sedes: print(s)
            input("\nPresione Enter para continuar...")

        elif opcion == '2':
            print(">>> CALCULANDO ASIGNACIÓN ÓPTIMA MÉTODO HÚNGARO <<<\n")
            
            # Asegurarse de que el número de tareas no sea mayor al de programadores
            if len(tareas) > len(programadores):
                print("Advertencia: Hay más tareas que programadores. No todas las tareas podrán ser asignadas.")
                input("\nPresione Enter para continuar...")
                continue
            
            hungaro = MetodoHungaro(programadores, tareas)
            
            # Mostrar matriz de costos inicial
            nombres_programadores = [p.nombre for p in programadores]
            nombres_tareas = [t.nombre for t in tareas]
            mostrar_matriz("Matriz de Costos de Contratación", hungaro.matriz_costos, nombres_programadores, nombres_tareas)

            asignaciones_optimas, costo_contratacion_total, programadores_contratados = hungaro.resolver()

            print("\n--- Resultados de la Asignación ---")
            for prog, tarea, costo in asignaciones_optimas:
                print(f"  - Programador '{prog.nombre}' asignado a Tarea '{tarea.nombre}' (Costo: ${costo:,.2f})")
            
            print("\n-------------------------------------------------")
            print(f"Costo Total de Contratación: ${costo_contratacion_total:,.2f}")
            print("-------------------------------------------------")
            input("\nPresione Enter para continuar...")

        elif opcion == '3':
            if not programadores_contratados:
                print("Error: Primero debe ejecutar la asignación de tareas (Opción 2) para saber qué programadores fueron contratados.")
                input("\nPresione Enter para continuar...")
                continue

            print(">>> CALCULANDO DISTRIBUCIÓN ÓPTIMA PROBLEMA DE TRANSPORTE <<<\n")

            demanda_total = sum(s.programadores_requeridos for s in sedes)
            oferta_total = len(programadores_contratados)

            if oferta_total < demanda_total:
                print(f"Advertencia: La oferta de programadores contratados ({oferta_total}) es menor que la demanda total de las sedes ({demanda_total}).")
                input("\nPresione Enter para continuar...")
                continue
            
            # Filtrar la matriz de costos de traslado para incluir solo a los programadores contratados
            indices_contratados = [programadores.index(p) for p in programadores_contratados]
            costos_filtrados = np.array(costos_traslado_ejemplo)[indices_contratados]
            
            transporte = ProblemaTransporte(programadores_contratados, sedes, costos_filtrados)
            
            nombres_contratados = [p.nombre for p in programadores_contratados]
            nombres_sedes = [s.nombre for s in sedes]
            mostrar_matriz("Matriz de Costos de Traslado", transporte.matriz_costos_traslado, nombres_contratados, nombres_sedes)

            distribucion_optima, costo_traslado_total, mensaje = transporte.resolver()
            
            print(f"\nEstado de la solución: {mensaje}")
            if distribucion_optima:
                print("\n--- Resultados de la Distribución ---")
                for prog, sede, costo in distribucion_optima:
                    print(f"  - Programador '{prog.nombre}' distribuido a Sede '{sede.nombre}' (Costo Traslado: ${costo:,.2f})")
                
                print("\n-------------------------------------------------")
                print(f"Costo Total de Traslado: ${costo_traslado_total:,.2f}")
                print("-------------------------------------------------")

            input("\nPresione Enter para continuar...")

        elif opcion == '4':
            limpiar_consola()
            print(">>> REPORTE FINAL <<<\n")
            if not asignaciones_optimas and not distribucion_optima:
                print("No hay datos calculados para generar un reporte. Por favor, ejecute las opciones 2 y 3.")
            else:
                mensaje_reporte = generar_reporte(asignaciones_optimas, costo_contratacion_total, distribucion_optima, costo_traslado_total)
                print(mensaje_reporte)
            input("\nPresione Enter para continuar...")

        elif opcion == '5':
            break
        else:
            input("Opción no válida. Presione Enter para intentar de nuevo...")

if __name__ == "__main__":
    main()