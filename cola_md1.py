class MD1Queue:
    def __init__(self, llegadas_totales, tiempo_observacion, atendidos_totales, tiempo_servicio):
        # Validación de entrada: verificar que todos los inputs sean > 0
        if llegadas_totales <= 0:
            raise ValueError("llegadas_totales debe ser mayor que 0.")
        if tiempo_observacion <= 0:
            raise ValueError("tiempo_observacion debe ser mayor que 0.")
        if atendidos_totales <= 0:
            raise ValueError("atendidos_totales debe ser mayor que 0.")
        if tiempo_servicio <= 0:
            raise ValueError("tiempo_servicio debe ser mayor que 0.")

        # Calcular la tasa de llegada (λ) y la tasa de servicio (μ)
        self.tasa_llegada = float(llegadas_totales) / float(tiempo_observacion)  # λ
        self.tasa_servicio = float(atendidos_totales) / float(tiempo_servicio)  # μ

        # Manejo de errores: verificar división por cero en utilización
        if self.tasa_servicio == 0:
            raise ValueError("La tasa de servicio no puede ser cero.")

        # Calcular la utilización del sistema (ρ)
        self.utilizacion = self.tasa_llegada / self.tasa_servicio

        # Verificar si el sistema es estable (ρ < 1)
        if self.utilizacion >= 1:
            raise ValueError("El sistema no es estable (ρ ≥ 1). La tasa de llegada debe ser menor que la tasa de servicio.")

        # Validación para evitar ZeroDivisionError en cálculos posteriores
        if self.tasa_servicio - self.tasa_llegada <= 0:
            raise ValueError("La diferencia (μ - λ) debe ser mayor que 0 para evitar división por cero.")

    def clientes_promedio_cola(self):
        """Número promedio de clientes en la cola (Lq)."""
        return (self.tasa_llegada ** 2) / (2 * self.tasa_servicio * (self.tasa_servicio - self.tasa_llegada))

    def clientes_promedio_sistema(self):
        """Número promedio de clientes en el sistema (L)."""
        return self.clientes_promedio_cola() + self.tasa_llegada / self.tasa_servicio

    def tiempo_espera_cola(self):
        """Tiempo promedio de espera en la cola (Wq)."""
        return self.clientes_promedio_cola() / self.tasa_llegada

    def tiempo_espera_sistema(self):
        """Tiempo promedio de espera en el sistema (W)."""
        return self.tiempo_espera_cola() + 1 / self.tasa_servicio


def presentar_resultados(cola: MD1Queue):
    """Presenta los resultados del sistema M/D/1."""
    print(f"Tasa de llegada (λ): {cola.tasa_llegada:.4f} clientes por unidad de tiempo")
    print(f"Tasa de servicio (μ): {cola.tasa_servicio:.4f} clientes atendidos por unidad de tiempo")
    print(f"Utilización del sistema (ρ): {cola.utilizacion:.4f}")
    print(f"Número promedio de clientes en la cola (Lq): {cola.clientes_promedio_cola():.4f}")
    print(f"Número promedio de clientes en el sistema (Ls): {cola.clientes_promedio_sistema():.4f}")
    print(f"Tiempo promedio de espera en la cola (Wq): {cola.tiempo_espera_cola():.4f} unidades de tiempo")
    print(f"Tiempo promedio de espera en el sistema (Ws): {cola.tiempo_espera_sistema():.4f} unidades de tiempo")


# Ejemplo de uso
if __name__ == "__main__":
    try:
        # Pedir al usuario los datos necesarios
        llegadas_totales = float(input("Ingrese el número total de llegadas observadas: "))
        tiempo_observacion = float(input("Ingrese el tiempo total de observación: "))
        atendidos_totales = float(input("Ingrese el número total de clientes atendidos: "))
        tiempo_servicio = float(input("Ingrese el tiempo total de servicio observado: "))

        # Crear una instancia del sistema M/D/1
        cola_md_1 = MD1Queue(llegadas_totales, tiempo_observacion, atendidos_totales, tiempo_servicio)

        # Mostrar los resultados
        presentar_resultados(cola_md_1)
    except ValueError as e:
        print(f"Error: {e}")