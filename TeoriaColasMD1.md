# Fórmulas M/D/1

## Variables
Tasa media de llegadas (λ): Cuántos clientes entran al sistema.
Tasa media de servicio (μ): Capacidad de atención de un solo servidor. El tiempo de servicio es constante e igual a 1/μ.
Número de servidores(s): Cantidad de canales de atención en paralelo. 
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

## Medidas del desempeño del sistema de colas
- Probabilidad de que el sistema esté vacío (P_0):

P_0 = 1 - ρ

- - Probabilidad de que haya n clientes en el sistema (P_n):

P_n = P^n * P_0

- Número esperado de clientes en la cola (L_q):
L_q = ρ^2 / (2 * (1 - ρ))

L_q = λ^2 / (2μ * (μ - λ))

- Número esperado de clientes en el sistema (L_s):
L_s = L_q + ρ

- Tiempo esperado de espera en la cola (W_q):
W_q = L_q / λ

W_q = ρ^2 / (2λ * (1 - ρ))

W_q = ρ / (2μ * (1 - ρ))


- Tiempo esperado de espera en el sistema (W_s):

W_s = L_s / λ

W_s = W_q + (1 / μ)

W_s = ρ / (2μ * (1 - ρ)) + (1 / μ)