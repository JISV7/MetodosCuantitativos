import datetime

def generar_reporte(asignaciones_hungaro, costo_hungaro, distribucion_transporte, costo_transporte, nombre_archivo="reporte.txt"):
    """
    Genera un reporte detallado en un .txt con la optimización.
    """
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("      REPORTE DE ASIGNACIÓN Y DISTRIBUCIÓN DE PROGRAMADORES\n")
            f.write("="*60 + "\n")
            f.write(f"Fecha de generación: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # --- Sección 1: Método Húngaro (Asignación Tarea-Programador) ---
            f.write("="*60 + "\n")
            f.write("1. Asignación Óptima de Tareas (Método Húngaro)\n")
            if not asignaciones_hungaro:
                f.write("No se realizaron asignaciones.\n")
            else:
                for prog, tarea, costo in asignaciones_hungaro:
                    f.write(f"- Programador '{prog.nombre}' asignado a Tarea '{tarea.nombre}'\n")
                    f.write(f"  (Habilidad requerida: {tarea.habilidad_requerida}, Costo de contratación: ${costo:,.2f})\n\n")
            f.write(f"Costo Total de Contratación: ${costo_hungaro:,.2f}\n")
            f.write("="*60 + "\n")

            # --- Sección 2: Problema de Transporte (Distribución a Sedes) ---
            f.write("="*60 + "\n")
            f.write("2. Distribución Óptima de Programadores a Sedes (Problema de Transporte)\n")

            if not distribucion_transporte:
                 f.write("No se realizó la distribución de programadores.\n")
            else:
                for prog, sede, costo in distribucion_transporte:
                    f.write(f"- Programador '{prog.nombre}' distribuido a Sede '{sede.nombre}' ({sede.localizacion})\n")
                    f.write(f"  (Costo de traslado: ${costo:,.2f})\n\n")

            f.write(f"Costo Total de Traslado: ${costo_transporte:,.2f}\n")
            f.write("="*60 + "\n")

            # --- Sección 3: Resumen General ---
            f.write("="*60 + "\n")
            f.write("RESUMEN GENERAL DE COSTOS\n")
            f.write("\n")
            f.write(f"Costo Total (Contratación + Traslado): ${costo_hungaro + costo_transporte:,.2f}\n")
            f.write("="*60 + "\n")
        
        return f"Reporte generado exitosamente en '{nombre_archivo}'"
    except IOError as e:
        return f"Error al escribir el archivo de reporte: {e}"