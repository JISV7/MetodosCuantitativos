# Modelos Deterministicos
D = Demanda anual
S = Costo de Pedido
H = Costo de mantener una unidad en inventario por año
CT= Costo total en modelo de inventario

d = Demanda diaria
LT = Lead Time (tiempo de entrega del pedido)

i = porcentaje de costo por mantener el inventario
C = Costo unitario de la compra


## Un solo Artículo Demanda constante
La cantidad a pedir en cada ocasión
Q = sqrt(2DS / H)

Punto de Reorden (ROP)
ROP=d×LT

d = D / numero de periodos

H = i * C

CT = (D / Q * S) + (Q / 2 * H) + (D * C)

### Costo total de pedidos en un año
D / Q * S

### Costo de almacenamiento para un año
Q / 2 * H

## Quiebre de precios
Se utilizan las mismas fórmulas, pero con cada precio correspondiente a cada rebaja.

## Varios Artículos con restricciones

# Modelos Probabilísticos.
μLT es la demanda promedio durante el tiempo de entrega.
σLT es la desviación estándar de la demanda durante el tiempo de entrega.
Z es el valor de Z correspondiente al nivel de servicio deseado

## Demanda y tiempo de entrega constante:

### Calcular punto de reorden
r = μLT + Z * σLT

### Calcular la demanda promedio durante el tiempo de entrega (μLT)
μLT = μ * LT

### Calcular la desviación estándar de la demanda durante el tiempo de entrega (σLT)
σLT = σ * sqrt(LT)

### Calcular la Cantidad de Pedido Óptima (EOQ)
EOQ = sqrt(2DS / H)