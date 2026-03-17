"""
Sistema M/D/1 - Análisis de mejora del tiempo medio
Problema 2: Servidor web corporativo
"""

import math


class MD1Queue:
    def __init__(self, tasa_llegada, tasa_servicio):
        """
        Inicializa el sistema M/D/1 con tasas dadas.
        :param tasa_llegada: λ (clientes por unidad de tiempo)
        :param tasa_servicio: μ (clientes por unidad de tiempo)
        """
        if tasa_llegada <= 0 or tasa_servicio <= 0:
            raise ValueError("Las tasas deben ser positivas.")
        if tasa_llegada >= tasa_servicio:
            raise ValueError("El sistema es inestable: λ ≥ μ. Debe cumplirse λ < μ.")

        self.tasa_llegada = tasa_llegada
        self.tasa_servicio = tasa_servicio
        self.utilizacion = tasa_llegada / tasa_servicio

    def clientes_promedio_cola(self):
        """Lq = λ² / (2 μ (μ - λ))"""
        return (self.tasa_llegada**2) / (
            2 * self.tasa_servicio * (self.tasa_servicio - self.tasa_llegada)
        )

    def clientes_promedio_sistema(self):
        """L = Lq + λ/μ"""
        return self.clientes_promedio_cola() + self.utilizacion

    def tiempo_espera_cola(self):
        """Wq = Lq / λ"""
        return self.clientes_promedio_cola() / self.tasa_llegada

    def tiempo_espera_sistema(self):
        """W = Wq + 1/μ"""
        return self.tiempo_espera_cola() + 1 / self.tasa_servicio

    def mostrar_medidas(self):
        """Imprime todas las medidas de desempeño."""
        print("\n--- Medidas de eficiencia M/D/1 ---")
        print(f"Tasa de llegada (λ): {self.tasa_llegada:.4f} clientes/min")
        print(f"Tasa de servicio (μ): {self.tasa_servicio:.4f} clientes/min")
        print(f"Utilización (ρ): {self.utilizacion:.4f}")
        print(f"Clientes promedio en cola (Lq): {self.clientes_promedio_cola():.4f}")
        print(
            f"Clientes promedio en sistema (L): {self.clientes_promedio_sistema():.4f}"
        )
        print(f"Tiempo promedio en cola (Wq): {self.tiempo_espera_cola():.4f} min")
        print(f"Tiempo promedio en sistema (W): {self.tiempo_espera_sistema():.4f} min")


def obtener_tasa_desde_intervalo(intervalo):
    """Convierte un intervalo de tiempo (minutos entre llegadas o servicio) en tasa."""
    return 1.0 / intervalo


def main():
    print("=== Análisis de sistema M/D/1 ===")
    print("El modelo M/D/1 supone llegadas Poisson y tiempo de servicio constante.")

    # Entrada de datos (puede ser por intervalo o tasa directa)
    print("\nIngrese los datos del sistema:")
    opcion = input("¿Desea ingresar tasas (λ, μ) o intervalos? (t/i): ").strip().lower()

    if opcion == "t":
        tasa_llegada = float(input("Tasa de llegada λ (clientes/min): "))
        tasa_servicio = float(input("Tasa de servicio μ (clientes/min): "))
    else:
        intervalo_llegadas = float(input("Intervalo medio entre llegadas (min): "))
        intervalo_servicio = float(input("Tiempo de servicio constante (min): "))
        tasa_llegada = obtener_tasa_desde_intervalo(intervalo_llegadas)
        tasa_servicio = obtener_tasa_desde_intervalo(intervalo_servicio)

    try:
        cola = MD1Queue(tasa_llegada, tasa_servicio)
        cola.mostrar_medidas()
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Análisis de mejora
    print("\n--- Análisis de mejora ---")
    print("Objetivo: Reducir el tiempo medio en el sistema (W).")
    objetivo = float(
        input("Ingrese el tiempo máximo deseado en sistema (min) [ej. 5]: ")
    )

    # Verificar si ya se cumple
    if cola.tiempo_espera_sistema() <= objetivo:
        print(
            f"El tiempo actual W = {cola.tiempo_espera_sistema():.4f} min ya es menor o igual a {objetivo} min."
        )
    else:
        print(
            f"El tiempo actual W = {cola.tiempo_espera_sistema():.4f} min supera el objetivo."
        )
        print(
            "Para mejorarlo, se puede aumentar la tasa de servicio (reducir tiempo de servicio)."
        )

        # Calcular la tasa de servicio necesaria para alcanzar el objetivo
        # La ecuación: W = Wq + 1/μ, con Wq = λ/(2μ(μ-λ))? No, Lq = λ²/(2μ(μ-λ)), Wq = λ/(2μ(μ-λ))
        # Entonces W = λ/(2μ(μ-λ)) + 1/μ = (λ + 2(μ-λ)) / (2μ(μ-λ))? Mejor resolver numéricamente.
        # Buscamos μ > λ tal que W(μ) = objetivo.
        # W(μ) = λ/(2μ(μ-λ)) + 1/μ = (λ + 2(μ-λ)) / (2μ(μ-λ))? Simplifiquemos:
        # W = (λ/(2μ(μ-λ))) + 1/μ = (λ + 2(μ-λ)) / (2μ(μ-λ))? No, porque 1/μ = 2(μ-λ)/(2μ(μ-λ))? En realidad, común denominador 2μ(μ-λ):
        # 1/μ = 2(μ-λ) / (2μ(μ-λ)), entonces suma: (λ + 2(μ-λ)) / (2μ(μ-λ)) = (2μ - λ) / (2μ(μ-λ))
        # Por lo tanto, W = (2μ - λ) / (2μ(μ-λ)). Igualamos a objetivo T:
        # (2μ - λ) = 2T μ (μ-λ) => 2μ - λ = 2T μ² - 2T λ μ => 0 = 2T μ² - 2T λ μ - 2μ + λ
        # => 2T μ² - (2T λ + 2) μ + λ = 0. Es una ecuación cuadrática en μ.
        # Resolvemos: A = 2T, B = -(2T λ + 2), C = λ.
        # μ = [ -B ± sqrt(B² - 4AC) ] / (2A) con signo positivo y mayor que λ.

        T = objetivo
        lam = cola.tasa_llegada
        A = 2 * T
        B = -(2 * T * lam + 2)
        C = lam
        discriminante = B**2 - 4 * A * C
        if discriminante < 0:
            print(
                "No es posible alcanzar el objetivo con este modelo (solución no real)."
            )
        else:
            mu1 = (-B + math.sqrt(discriminante)) / (2 * A)
            mu2 = (-B - math.sqrt(discriminante)) / (2 * A)
            # Elegir la que sea mayor que lam
            mu_necesaria = None
            for mu in (mu1, mu2):
                if mu > lam:
                    mu_necesaria = mu
                    break
            if mu_necesaria is None:
                print("No se encontró una tasa de servicio factible.")
            else:
                print(
                    f"Para lograr W = {T} min, se necesita μ = {mu_necesaria:.4f} clientes/min"
                )
                print(
                    f"Eso equivale a un tiempo de servicio de {1 / mu_necesaria:.4f} min por cliente."
                )
                print(
                    f"La tasa actual es μ = {cola.tasa_servicio:.4f} (tiempo de servicio = {1 / cola.tasa_servicio:.4f} min)."
                )

    # Opción de probar cambios manualmente
    print("\n¿Desea probar con otra tasa de servicio? (s/n)")
    resp = input().strip().lower()
    while resp == "s":
        nueva_mu = float(input("Ingrese nueva tasa de servicio μ (clientes/min): "))
        try:
            nueva_cola = MD1Queue(cola.tasa_llegada, nueva_mu)
            nueva_cola.mostrar_medidas()
            if nueva_cola.tiempo_espera_sistema() <= objetivo:
                print("¡Se cumple el objetivo!")
            else:
                print("Aún no se cumple el objetivo.")
        except ValueError as e:
            print(f"Error: {e}")
        print("\n¿Otra prueba? (s/n)")
        resp = input().strip().lower()

    print("\n--- Fin del análisis ---")


if __name__ == "__main__":
    main()
