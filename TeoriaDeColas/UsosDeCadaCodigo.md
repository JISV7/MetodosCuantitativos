Los cuatro códigos que tienes implementan diferentes modelos de teoría de colas, cada uno con supuestos distintos sobre la distribución de los tiempos de servicio y la cantidad de servidores. A continuación te explico cuándo usar cada uno.

---

## 1. **`cola_mm1.py` – Modelo M/M/1**
- **Supuestos**:
  - Llegadas: Proceso de Poisson (tiempos entre llegadas exponenciales).
  - Servicio: Tiempos de servicio exponenciales.
  - Un solo servidor.
- **Cuándo usarlo**:
  - Cuando hay **un único canal de atención** (ej. una ventanilla, una caja registradora).
  - Las llegadas son aleatorias e independientes.
  - El tiempo que toma atender a cada cliente varía de forma exponencial (mucha variabilidad, algunos muy cortos, otros muy largos).
- **Qué calcula**: Tasa de llegada (λ), tasa de servicio (μ), utilización (ρ), número promedio de clientes en cola (Lq) y en sistema (L), tiempos promedio de espera en cola (Wq) y en sistema (W).

---

## 2. **`cola_md1.py` – Modelo M/D/1**
- **Supuestos**:
  - Llegadas: Proceso de Poisson.
  - Servicio: **Determinístico** (constante), todos los servicios duran exactamente el mismo tiempo.
  - Un solo servidor.
- **Cuándo usarlo**:
  - Cuando el tiempo de servicio es **fijo o constante**.
  - Ejemplos: una máquina que siempre tarda 2 minutos en procesar una pieza, un peaje automático con duración fija, un torniquete que deja pasar personas a intervalos regulares.
  - La variabilidad del servicio es cero (a diferencia del M/M/1).
- **Qué calcula**: Las mismas métricas que M/M/1, pero con fórmulas específicas para servicio constante.

---

## 3. **`cola_mmc.py` – Modelo M/M/c**
- **Supuestos**:
  - Llegadas: Proceso de Poisson.
  - Servicio: Tiempos exponenciales (todos los servidores tienen la misma tasa μ).
  - **Múltiples servidores en paralelo** (c servidores).
- **Cuándo usarlo**:
  - Cuando hay **varios canales de atención idénticos** que trabajan simultáneamente (ej. banco con varias ventanillas, call center con varios agentes).
  - Las llegadas son aleatorias, los tiempos de servicio también son exponenciales.
  - Los clientes forman una sola cola y pasan al primer servidor disponible.
- **Qué calcula**: Además de λ, μ, ρ, calcula la probabilidad de que el sistema esté vacío (P0), y luego Lq, L, Wq, W usando fórmulas que involucran factoriales y sumatorias.

---

## 4. **`probabilidadEstadomms.py` – Probabilidades de estado Pₙ**
- **Supuestos**: Es genérico para cualquier modelo **M/M/s** (puede ser uno o varios servidores).
- **Cuándo usarlo**:
  - Cuando necesitas conocer la **distribución de probabilidad del número de clientes** en el sistema, es decir, la probabilidad de que haya exactamente n clientes (Pₙ).
  - No calcula directamente L, Lq, W, Wq (aunque se podrían derivar), sino que te da la probabilidad para cada estado n.
  - Es útil para análisis más detallados, como determinar la probabilidad de que la cola exceda cierto tamaño, o para validar otros cálculos.
- **Observación**: La función `p0` incluida calcula la probabilidad de sistema vacío, necesaria para las Pₙ. El código de ejemplo muestra Pₙ para n desde 0 hasta 44.

---

### Resumen de aplicación práctica
| Situación | Modelo a usar |
|-----------|---------------|
| Un cajero, llegadas aleatorias, tiempos de servicio variables (exponenciales) | **M/M/1** (`cola_mm1.py`) |
| Un cajero, llegadas aleatorias, tiempo de servicio fijo (constante) | **M/D/1** (`cola_md1.py`) |
| Varios cajeros en paralelo, llegadas aleatorias, tiempos de servicio exponenciales | **M/M/c** (`cola_mmc.py`) |
| Necesito la probabilidad de que haya exactamente n clientes (para cualquier s) | **probabilidadEstadomms.py** |

Si tienes dudas sobre cómo interpretar los resultados o cómo ajustar los parámetros, comenta y te ayudo.