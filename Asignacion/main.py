# Alejandro Lopez 30914440
# Jose Sanchez 30958324
import numpy as np
import os
# python -m venv .env
# python -m pip install numpy
from models import Programador, Tarea, Sede
from optimizer import Optimizador

class SistemaAsignacion:
    """Sistema principal para gestionar la asignación y contratación."""
    
    def __init__(self):
        self.programadores = []
        self.tareas = []
        self.sedes = []
        self.matriz_costos_asignacion = np.array([])
        self.resultados_hungaro = {}
        self.resultados_transporte = {}

    def limpiar_consola(self):
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu_principal(self):
        """Muestra el menú principal y gestiona la entrada del usuario."""
        while True:
            self.limpiar_consola()
            print("===== Sistema de Asignación y Contratación de Programadores =====")
            print("1. Ingresar Datos (Programadores, Tareas, Sedes)")
            print("2. Resolver Asignación Programador-Tarea (Método Húngaro)")
            print("3. Resolver Distribución a Sedes (Problema de Transporte)")
            print("4. Generar Reporte Final")
            print("5. Salir")
            print("=" * 65)
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == '1':
                self.ingresar_datos()
            elif opcion == '2':
                self.ejecutar_asignacion_hungara()
            elif opcion == '3':
                self.ejecutar_distribucion_transporte()
            elif opcion == '4':
                self.generar_reporte_final()
            elif opcion == '5':
                print("Saliendo del sistema.")
                break
            else:
                input("Opción no válida. Presione Enter para continuar...")

    def ingresar_datos(self):
        """Permite al usuario ingresar programadores, tareas y sedes con manejo de errores."""
        self.limpiar_consola()
        print("--- Módulo de Ingreso de Datos ---")

        # --- Entrada de Programadores ---
        while True:
            try:
                num = int(input("¿Cuántos programadores desea ingresar? "))
                if num < 0:
                    print("Error: Por favor, ingrese un número no negativo.")
                    continue
                break
            except ValueError:
                print("Error: Entrada inválida. Por favor, ingrese un número entero.")
        
        self.programadores = []  # Limpiar la lista para nuevos ingresos
        for i in range(num):
            nombre = input(f"  Nombre del Programador {i+1}: ").strip()
            while not nombre: # Valida que el nombre no esté vacío
                print("Error: El nombre no puede estar vacío.")
                nombre = input(f"  Nombre del Programador {i+1}: ").strip()
            habilidades = input("  Habilidades (separadas por coma): ").split(',')
            self.programadores.append(Programador(nombre, [h.strip() for h in habilidades]))
        
        print("\n---")
        
        # --- Entrada de Tareas ---
        while True:
            try:
                num = int(input("¿Cuántas tareas desea ingresar? "))
                if num < 0:
                    print("Error: Por favor, ingrese un número no negativo.")
                    continue
                break
            except ValueError:
                print("Error: Entrada inválida. Por favor, ingrese un número entero.")

        self.tareas = []  # Limpiar la lista para nuevos ingresos
        for i in range(num):
            nombre = input(f"  Nombre de la Tarea {i+1}: ").strip()
            while not nombre: # Valida que el nombre no esté vacío
                print("Error: El nombre no puede estar vacío.")
                nombre = input(f"  Nombre de la Tarea {i+1}: ").strip()
            self.tareas.append(Tarea(nombre))

        print("\n---")
        
        # --- Entrada de Sedes ---
        while True:
            try:
                num = int(input("¿Cuántas sedes/proyectos desea ingresar? "))
                if num < 0:
                    print("Error: Por favor, ingrese un número no negativo.")
                    continue
                break
            except ValueError:
                print("Error: Entrada inválida. Por favor, ingrese un número entero.")

        self.sedes = []  # Limpiar la lista para nuevos ingresos
        for i in range(num):
            nombre = input(f"  Nombre de la Sede {i+1}: ").strip()
            while not nombre: # Valida que el nombre no esté vacío
                print("Error: El nombre no puede estar vacío.")
                nombre = input(f"  Nombre de la Sede {i+1}: ").strip()
            localizacion = input("  Localización: ")
            
            while True:
                try:
                    requeridos = int(input(f"  Programadores requeridos para '{nombre}': "))
                    if requeridos < 0:
                        print("Error: El número de programadores requeridos no puede ser negativo.")
                        continue
                    break
                except ValueError:
                    print("Error: Entrada inválida. Por favor, ingrese un número entero.")
            self.sedes.append(Sede(nombre, localizacion, requeridos))

        input("\nDatos guardados exitosamente. Presione Enter para volver al menú...")

    def ejecutar_asignacion_hungara(self):
        """Gestiona la ejecución del Método Húngaro."""
        self.limpiar_consola()
        print("--- Método Húngaro: Asignación Programador <-> Tarea ---")

        if not self.programadores or not self.tareas:
            input("Error: Debe ingresar programadores y tareas primero (Opción 1). Presione Enter...")
            return

        num_programadores = len(self.programadores)
        num_tareas = len(self.tareas)
        matriz = []
        for i, prog in enumerate(self.programadores):
            fila_actual = []
            print(f"\n--- Costos para {prog.nombre} ---")
            for j, tarea in enumerate(self.tareas):
                while True:
                    try:
                        costo = float(input(f"  Costo para la Tarea '{tarea.nombre}': "))
                        fila_actual.append(costo)
                        break
                    except ValueError:
                        print("Error: Ingrese un número válido.")
            matriz.append(fila_actual)
        
        self.matriz_costos_asignacion = np.array(matriz)
        
        filas, cols, costo_total = Optimizador.metodo_hungaro(self.matriz_costos_asignacion)

        self.resultados_hungaro = {"filas": filas, "columnas": cols, "costo_total": costo_total}
        print("\n" + "="*50)
        print("--- Asignación Óptima Encontrada ---")
        for fila, col in zip(filas, cols):
            print(f"{self.programadores[fila].nombre} --> {self.tareas[col].nombre} (Costo: {self.matriz_costos_asignacion[fila, col]})")
        print(f"\nCosto Total Mínimo de Contratación: {costo_total}")

        input("\nPresione Enter para volver al menú...")

    def ejecutar_distribucion_transporte(self):
        """Gestiona la ejecución del Problema de Transporte."""
        self.limpiar_consola()
        print("--- Problema de Transporte: Distribución a Sedes ---")

        if not self.programadores or not self.sedes:
            input("Error: Debe ingresar programadores y sedes primero (Opción 1). Presione Enter...")
            return

        oferta = [1] * len(self.programadores)
        demanda = [s.programadores_requeridos for s in self.sedes]
        costos_transporte = []
        
        # Comprobación de oferta vs demanda
        if sum(oferta) < sum(demanda):
            print("\nADVERTENCIA: La oferta de programadores es menor que la demanda total de las sedes.")
            print(f"Oferta total: {sum(oferta)}, Demanda total: {sum(demanda)}")
            input("No se puede encontrar una solución. Presione Enter para volver...")
            return
            
        for i, prog in enumerate(self.programadores):
            fila_costos = []
            print(f"\nCostos de traslado para {prog.nombre}:")
            for j, sede in enumerate(self.sedes):
                while True:
                    try:
                        costo = float(input(f"  Costo para enviar a la sede '{sede.nombre}': "))
                        fila_costos.append(costo)
                        break
                    except ValueError:
                        print("Error: Ingrese un número válido.")
            costos_transporte.append(fila_costos)
        
        self.resultados_transporte = Optimizador.problema_transporte(np.array(costos_transporte), oferta, demanda)

        print("\n" + "="*50)
        print("--- Distribución Óptima Encontrada ---")
        if self.resultados_transporte["exito"]:
            flujo = self.resultados_transporte["flujo"]
            for i in range(len(self.programadores)):
                for j in range(len(self.sedes)):
                    if flujo[i, j] > 0: # Si hay una asignación
                        print(f"Asignar a {self.programadores[i].nombre} a la sede '{self.sedes[j].nombre}' (Cantidad: {flujo[i, j]:.0f})")
            print(f"\nCosto Total Mínimo de Distribución: {self.resultados_transporte['costo']}")
        else:
            print(f"No se pudo encontrar una solución: {self.resultados_transporte['mensaje']}")

        input("\nPresione Enter para volver al menú...")

    def generar_reporte_final(self):
        """Genera un reporte en consola y lo exporta a un archivo TXT."""
        self.limpiar_consola()
        print("--- Generando Reporte Final ---")
        
        reporte_contenido = [
            "="*60,
            "    REPORTE DE ASIGNACIÓN Y CONTRATACIÓN ÓPTIMA",
            "="*60
        ]

        if self.resultados_hungaro:
            reporte_contenido.extend([
                "\n1. MATRIZ DE COSTOS DE ASIGNACIÓN (PROGRAMADOR vs TAREA)",
                str(self.matriz_costos_asignacion),
                "\n\n2. DECISIONES DE CONTRATACIÓN Y ASIGNACIÓN (MÉTODO HÚNGARO)"
            ])
            filas, cols = self.resultados_hungaro['filas'], self.resultados_hungaro['columnas']
            for fila, col in zip(filas, cols):
                linea = f"- Asignar a {self.programadores[fila].nombre} la tarea '{self.tareas[col].nombre}'. Costo: {self.matriz_costos_asignacion[fila, col]}"
                reporte_contenido.append(linea)
            reporte_contenido.extend([
                "\n" + "-"*60,
                f"COSTO TOTAL MÍNIMO DE ASIGNACIÓN: {self.resultados_hungaro['costo_total']}",
                "-"*60
            ])
        else:
            reporte_contenido.append("\nNo se han calculado los resultados de asignación de tareas.")

        if self.resultados_transporte and self.resultados_transporte.get("exito"):
            reporte_contenido.append("\n\n3. DECISIONES DE DISTRIBUCIÓN A SEDES (PROBLEMA DE TRANSPORTE)")
            flujo = self.resultados_transporte["flujo"]
            for i in range(len(self.programadores)):
                for j in range(len(self.sedes)):
                    if flujo[i, j] > 0:
                        linea = f"- Enviar a {self.programadores[i].nombre} a la sede '{self.sedes[j].nombre}'."
                        reporte_contenido.append(linea)
            reporte_contenido.extend([
                "\n" + "-"*60,
                f"COSTO TOTAL MÍNIMO DE DISTRIBUCIÓN: {self.resultados_transporte['costo']}",
                "-"*60
            ])
        else:
            reporte_contenido.append("\n\nNo se han calculado los resultados de distribución a sedes.")

        nombre_archivo = "reporte_asignacion.txt"
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            for linea in reporte_contenido:
                print(linea)
                f.write(linea + "\n")
        
        print(f"\n\nReporte exportado exitosamente a '{nombre_archivo}'")
        input("\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    sistema = SistemaAsignacion()
    sistema.menu_principal()