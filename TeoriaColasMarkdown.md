# Fórmulas M/M/S

## Variables
Tasa media de llegadas (λ): Cuántos clientes entran al sistema.
Tasa media de servicio (μ): Capacidad de atención de un solo servidor.
Número de servidores(s): Cantidad de canales de atención en paralelo. 
Intensidad de tráfico (u)
Factor de Utilización (ρ)
Tiempo esperado entre llegadas (1 / λ)
Tiempo esperado de servicio (1 / μ)

## Índices
Probability (P): Probabilidad de que el sistema esté en un estado específico.
Length(L): Longitud o número esperado de clientes (cantidad de personas).
Wait (W): Tiempo esperado de espera (minutos, horas, etc.).

## Subíndices
Subíndices (¿Dónde lo medimos?)
s (System): En el sistema completo (Haciendo fila + Siendo atendidos).
q (Queue): En la cola o fila (Esperando ser atendidos).
0 (Zero): Estado vacío (Cero clientes en el sistema).
n (Number): Estado con exactamente n clientes.
w (Waiting/Wait): Probabilidad de esperar (cuando el sistema está lleno).
b (Busy): Periodo ocupado. Aquellos que encontraron el sistema lleno y tuvieron que esperar.

## Formas de evitar una cola:
λ < s * μ

## Factor de Utilización
ρ = λ / (s * μ)

## Intensidad de tráfico
u = λ / μ

## Medidas del desempeño del sistema de colas
- Probabilidad de que el sistema esté vacío (P_0)
P_0 = 1 / (Σ_{n=0}^{s-1} ((λ / μ)^n / n!) + ((λ / μ)^s / s!) * ((s * μ) / (s * μ - λ)))

- Probabilidad de que haya n clientes en el sistema (P_n)
Para n >= s
P_n = ((λ / μ)^n / (s! * s^(n-s))) * P_0

Para n < s
P_n = ((λ / μ)^n / (n!)) * P_0

- Probabilidad de que un cliente deba esperar (P_w):
P_w = Σ_{n=s}^{∞} P_n

P_w = (((λ / μ)^s / s!) * ((s * μ) / (s * μ - λ))) * P_0

- Número esperado de clientes en la cola (L_q):
L_q = λ * W_q

L_q = (1 / s!) * ((λ / μ)^s) * (ρ / (1 - ρ)^2) * P_0

L_q = Σ_{n=s}^{∞} (n - s) * P_n

L_q = ((((λ / μ)^s) * λ * μ) / (s - 1)! * (s * μ - λ)^2) * P_0

L_q = P_w * (ρ / (1 - ρ))

L_q = λ * P_w * W_b

L_q = λ * W_q

- Número esperado de clientes en el sistema (L_s):
L_s = λ * W_s

L_s = L_q + (λ / μ)

L_s = Σ_{n=0}^{∞} n * P_n

L_s = λ * W_s

- Número promedio de clientes en la cola "Ocupada" (L_b):
L_b = L_q / P_w

- Tiempo esperado de espera en el sistema (W_s):
W_s = W_q + (1 / μ)

- Tiempo esperado de espera en la cola (W_q):
W_q = L_q / λ

- Tiempo esperado de espera para los que esperan (W_b)
W_b = W_q / P_w

W_b = 1 / (s * μ - λ)