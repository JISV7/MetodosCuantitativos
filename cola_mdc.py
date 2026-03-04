import math


class MDSQueue:
    def __init__(self, llegadas_totales, tiempo_observacion, atendidos_totales, tiempo_servicio, servidores):
        # Validación de entrada: verificar que todos los inputs sean > 0
        if llegadas_totales <= 0:
            raise ValueError("llegadas_totales debe ser mayor que 0.")
        if tiempo_observacion <= 0:
            raise ValueError("tiempo_observacion debe ser mayor que 0.")
        if atendidos_totales <= 0:
            raise ValueError("atendidos_totales debe ser mayor que 0.")
        if tiempo_servicio <= 0:
            raise ValueError("tiempo_servicio debe ser mayor que 0.")
        if servidores <= 0:
            raise ValueError("servidores debe ser mayor que 0.")

        # Calcular la tasa de llegada (λ) y la tasa de servicio (μ)
        self.tasa_llegada = float(llegadas_totales) / float(tiempo_observacion)  # λ
        self.tasa_servicio = float(atendidos_totales) / float(tiempo_servicio)  # μ
        self.servidores = int(servidores)  # c

        # Manejo de errores: verificar división por cero en utilización
        if self.tasa_servicio == 0:
            raise ValueError("La tasa de servicio no puede ser cero.")
        if self.servidores == 0:
            raise ValueError("El número de servidores no puede ser cero.")

        # Calcular la utilización del sistema (ρ)
        self.utilizacion = self.tasa_llegada / (self.servidores * self.tasa_servicio)

        # Verificar si el sistema es estable (ρ < 1)
        if self.utilizacion >= 1:
            raise ValueError("El sistema no es estable (ρ ≥ 1). La tasa de llegada debe ser menor que la tasa de servicio multiplicada por el número de servidores.")

        # Validación para evitar ZeroDivisionError en cálculos posteriores
        if 1 - self.utilizacion <= 0:
            raise ValueError("La diferencia (1 - ρ) debe ser mayor que 0 para evitar división por cero.")

    def probabilidad_sistema_vacio(self):
        """Probabilidad de que no haya clientes en el sistema (P0)."""
        sumatoria = sum([(self.tasa_llegada / self.tasa_servicio) ** n / math.factorial(n) for n in range(self.servidores)])
        segundo_termino = ((self.tasa_llegada / self.tasa_servicio) ** self.servidores) / (math.factorial(self.servidores) * (1 - self.utilizacion))
        P0 = 1 / (sumatoria + segundo_termino)
        return P0

    def clientes_promedio_cola(self):
        """Número promedio de clientes en la cola (Lq)."""
        # Aproximación para M/D/s: Lq ≈ 0.5 * Lq(M/M/s)
        P0 = self.probabilidad_sistema_vacio()
        Lq_mmc = (P0 * (self.tasa_llegada / self.tasa_servicio) ** self.servidores * self.utilizacion) / (math.factorial(self.servidores) * (1 - self.utilizacion) ** 2)
        return Lq_mmc * 0.5

    def clientes_promedio_sistema(self):
        """Número promedio de clientes en el sistema (L)."""
        return self.clientes_promedio_cola() + self.tasa_llegada / self.tasa_servicio

    def tiempo_espera_cola(self):
        """Tiempo promedio de espera en la cola (Wq)."""
        return self.clientes_promedio_cola() / self.tasa_llegada

    def tiempo_espera_sistema(self):
        """Tiempo promedio de espera en el sistema (W)."""
        return self.tiempo_espera_cola() + 1 / self.tasa_servicio


def presentar_resultados(cola: MDSQueue):
    """Presenta los resultados del sistema M/D/s."""
    print(f"Tasa de llegada (λ): {cola.tasa_llegada:.4f} clientes por unidad de tiempo")
    print(f"Tasa de servicio (μ): {cola.tasa_servicio:.4f} clientes atendidos por servidor por unidad de tiempo")
    print(f"Utilización del sistema (ρ): {cola.utilizacion:.4f}")
    print(f"Probabilidad de que el sistema esté vacío (P0): {cola.probabilidad_sistema_vacio():.4f}")
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
        servidores = int(input("Ingrese el número de servidores: "))

        # Crear una instancia del sistema M/D/s
        cola_md_s = MDSQueue(llegadas_totales, tiempo_observacion, atendidos_totales, tiempo_servicio, servidores)

        # Mostrar los resultados
        presentar_resultados(cola_md_s)
    except ValueError as e:
        print(f"Error: {e}")