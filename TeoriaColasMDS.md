# Fórmulas M/D/s

## Variables
Tasa media de llegadas (λ): Cuántos clientes entran al sistema.
Tasa media de servicio (μ): Capacidad de atención de un solo servidor.
Número de servidores (s): Cantidad de canales de atención en paralelo.
Factor de Utilización (ρ): Proporción de tiempo que cada servidor está ocupado.
Tiempo esperado entre llegadas (1 / λ)
Tiempo esperado de servicio, es constante (1 / μ)

## Índices
Probability (P): Probabilidad de que el sistema esté en un estado específico.
Length (L): Longitud o número esperado de clientes (cantidad de personas).
Wait (W): Tiempo esperado de espera (minutos, horas, etc.).

## Subíndices
(¿Dónde lo medimos?)
s (System): En el sistema completo (Haciendo fila + Siendo atendidos).
q (Queue): En la cola o fila (Esperando ser atendidos).
0 (Zero): Estado vacío (Cero clientes en el sistema).
n (Number): Estado con exactamente n clientes.
w (Waiting/Wait): Probabilidad de esperar (cuando el sistema está lleno).
b (Busy): Periodo ocupado. Aquellos que encontraron el sistema lleno y tuvieron que esperar.

## Factor de Utilización
ρ = λ / (s * μ)

## Intensidad de tráfico
u = λ / μ

## Medidas del desempeño del sistema de colas

- Probabilidad de que el sistema esté vacío (P_0):
P_0 = 1 / ((Σ_{n=0}^{s-1} ((λ / μ)^n / n!)) + ((λ / μ)^s / s!) * ((s * μ) / (s * μ - λ)))

- Probabilidad de que un cliente tenga que esperar (P_w):
P_w = ( (s * ρ)^s / ( s! * (1 - ρ) ) ) * P_0

- Número esperado de clientes en la cola (L_q):
L_q = ( (s * ρ)^s * ρ ) / ( s! * s * (1 - ρ)^2 ) * P_0 * (1/2)

- Número esperado de clientes en el sistema (L_s):
L_s = L_q + λ / μ

L_s = L_q + s * ρ

- Tiempo esperado de espera en la cola (W_q):
W_q = L_q / λ

- Tiempo esperado de espera en el sistema (W_s):
W_s = W_q + (1 / μ)