import math


class MMSCola:
    """Clase para calcular probabilidades en un sistema M/M/s."""

    def __init__(self, lmbda, mu, s):
        """
        Inicializa el sistema M/M/s.

        Args:
            lmbda: Tasa de llegada (λ)
            mu: Tasa de servicio por servidor (μ)
            s: Número de servidores

        Raises:
            ValueError: Si el sistema no es estable (λ ≥ s * μ)
        """
        # Validación de entrada
        if lmbda <= 0:
            raise ValueError("lmbda (tasa de llegada) debe ser mayor que 0.")
        if mu <= 0:
            raise ValueError("mu (tasa de servicio) debe ser mayor que 0.")
        if s <= 0:
            raise ValueError("s (número de servidores) debe ser mayor que 0.")

        self.lmbda = float(lmbda)
        self.mu = float(mu)
        self.s = int(s)

        # Intensidad de tráfico (u = λ / μ)
        self.intensidad = self.lmbda / self.mu

        # Utilización del sistema (ρ = λ / (s * μ))
        self.utilizacion = self.lmbda / (self.s * self.mu)

        # Manejo de estabilidad: lanzar ValueError si el sistema no es estable
        if self.lmbda >= self.s * self.mu:
            raise ValueError(
                f"El sistema no es estable. La tasa de llegada (λ={self.lmbda}) debe ser "
                f"menor que s * μ ({self.s * self.mu})."
            )

        # Calcular p0 una vez en la inicialización (evita redundancia)
        self.p_0 = self._calcular_p0()

    def _factorial(self, n):
        """Calcula factorial usando math.lgamma para mayor robustez numérica."""
        return math.exp(math.lgamma(n + 1))

    def _calcular_p0(self):
        """
        Calcula la probabilidad de que el sistema esté vacío (P0).

        Returns:
            float: Probabilidad P0
        """
        rho = self.intensidad  # u = λ / μ
        s = self.s

        # Sumatoria para n = 0 hasta s-1
        sum1 = sum((rho ** n) / self._factorial(n) for n in range(s))

        # Término para n >= s
        if self.utilizacion >= 1:
            return 0.0  # Sistema inestable, pero ya validado en __init__

        sum2 = (rho ** s) / (self._factorial(s) * (1 - self.utilizacion))

        return 1 / (sum1 + sum2)

    def p0(self):
        """Retorna la probabilidad de que el sistema esté vacío (P0)."""
        return self.p_0

    def pn(self, n):
        """
        Calcula la probabilidad de tener n clientes en el sistema.

        Args:
            n: Número de clientes

        Returns:
            float: Probabilidad Pn
        """
        if n < 0:
            raise ValueError("n debe ser un entero no negativo.")

        rho = self.intensidad  # u = λ / μ
        s = self.s

        if n < s:
            return (rho ** n / self._factorial(n)) * self.p_0
        else:
            return (rho ** n / (self._factorial(s) * (s ** (n - s)))) * self.p_0


def presentar_resultados(cola: MMSCola, n_max=100):
    """
    Presenta las probabilidades de estado estable.

    Args:
        cola: Instancia de MMSCola
        n_max: Número máximo de estados a mostrar (por defecto 100)
    """
    print(f"Tasa de llegada (λ): {cola.lmbda:.4f}")
    print(f"Tasa de servicio (μ): {cola.mu:.4f}")
    print(f"Número de servidores (s): {cola.s}")
    print(f"Intensidad de tráfico (u = λ/μ): {cola.intensidad:.4f}")
    print(f"Utilización del sistema (ρ = λ/(s*μ)): {cola.utilizacion:.4f}")
    print(f"Probabilidad de sistema vacío (P0): {cola.p0():.4f}")
    print(f"\nProbabilidades P(n) para n = 0 hasta {n_max}:")
    print("-" * 30)
    for n in range(n_max + 1):
        print(f"P({n:3d}) = {cola.pn(n):.4f}")


# Ejemplo de uso
if __name__ == "__main__":
    try:
        # Pedir al usuario los datos necesarios
        lmbda = float(input("Ingrese la tasa de llegada (λ): "))
        mu = float(input("Ingrese la tasa de servicio (μ): "))
        s = int(input("Ingrese el número de servidores (s): "))
        # rango máximo de estados a mostrar (por defecto 100)
        try:
            n_max = int(input("Ingrese el máximo n para mostrar P(n) [enter=100]: ") or 100)
        except ValueError:
            n_max = 100

        # Crear instancia del sistema M/M/s (p0 se calcula dinámicamente)
        cola = MMSCola(lmbda, mu, s)

        # Mostrar resultados
        presentar_resultados(cola, n_max)
    except ValueError as e:
        print(f"Error: {e}")
