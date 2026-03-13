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
        # Probabilidad de que todos los servidores estén ocupados (P(N ≥ s))
        self.p_ocupados = self._calcular_p_ocupados()

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

    def _calcular_p_ocupados(self):
        """
        Calcula la probabilidad de que todos los servidores estén ocupados (P(N ≥ s)).
        También conocida como fórmula C de Erlang.
        """
        return (self.p_0 * (self.intensidad ** self.s) /
                (self._factorial(self.s) * (1 - self.utilizacion)))

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

    def p_cola_mayor_n(self, n):
        """
        Probabilidad de que el número de clientes en la cola (esperando) sea mayor que n.
        P(Cola > n) = P(N ≥ s) * ρ^(n+1)

        Args:
            n: Número de clientes a partir del cual se mide la cola (n ≥ 0)

        Returns:
            float: Probabilidad
        """
        if n < 0:
            raise ValueError("n debe ser un entero no negativo.")
        return self.p_ocupados * (self.utilizacion ** (n + 1))

    def p_wq_mayor_t(self, t):
        """
        Probabilidad de que el tiempo de espera en cola sea mayor que t.
        P(W_q > t) = P(N ≥ s) * e^(-s μ (1-ρ) t)

        Args:
            t: Tiempo (t ≥ 0)

        Returns:
            float: Probabilidad
        """
        if t < 0:
            raise ValueError("t debe ser mayor o igual a 0.")
        tasa = self.s * self.mu * (1 - self.utilizacion)
        return self.p_ocupados * math.exp(-tasa * t)

    def p_ws_mayor_t(self, t):
        """
        Probabilidad de que el tiempo total en el sistema (cola + servicio) sea mayor que t.
        Para M/M/s se utiliza la fórmula derivada de la convolución.

        Args:
            t: Tiempo (t ≥ 0)

        Returns:
            float: Probabilidad
        """
        if t < 0:
            raise ValueError("t debe ser mayor o igual a 0.")

        rho = self.utilizacion
        s = self.s
        mu = self.mu
        p_ocup = self.p_ocupados
        factor = s * (1 - rho)  # s(1-ρ)

        # Caso especial cuando s(1-ρ) = 1 (límite)
        if abs(factor - 1.0) < 1e-12:
            return math.exp(-mu * t) * (1 + p_ocup * mu * t)
        else:
            beta = mu * (factor - 1)  # μ (s(1-ρ)-1)
            termino = (p_ocup / (factor - 1)) * (factor - math.exp(-beta * t))
            return math.exp(-mu * t) * (1 - p_ocup + termino)


def presentar_resultados(cola: MMSCola, n_max=100):
    """
    Presenta las probabilidades de estado estable y algunas métricas adicionales.

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
    print(f"Probabilidad de que todos los servidores estén ocupados (P(N≥s)): {cola.p_ocupados:.4f}")
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

        # Crear instancia del sistema M/M/s
        cola = MMSCola(lmbda, mu, s)

        # Mostrar resultados básicos
        presentar_resultados(cola, n_max)

        # Solicitar valores para calcular probabilidades adicionales
        print("\n--- Probabilidades adicionales ---")
        n_cola = int(input("Ingrese n para P(Cola > n): "))
        print(f"P(Cola > {n_cola}) = {cola.p_cola_mayor_n(n_cola):.6f}")

        t_wq = float(input("Ingrese t para P(W_q > t): "))
        print(f"P(W_q > {t_wq}) = {cola.p_wq_mayor_t(t_wq):.6f}")

        t_ws = float(input("Ingrese t para P(W_s > t): "))
        print(f"P(W_s > {t_ws}) = {cola.p_ws_mayor_t(t_ws):.6f}")

    except ValueError as e:
        print(f"Error: {e}")