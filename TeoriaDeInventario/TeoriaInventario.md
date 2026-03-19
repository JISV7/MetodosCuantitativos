La teoría de inventarios es un área de estudio dentro de la investigación operativa que se enfoca en cómo gestionar eficazmente los inventarios de productos o bienes en una empresa. El objetivo principal es determinar cuándo y cuánto ordenar para satisfacer la demanda, minimizando los costos asociados.

# Conceptos Básicos de la Teoría de Inventarios
Inventario: Se refiere a los bienes o materiales que una empresa tiene almacenados para su uso o venta. Puede incluir materias primas, productos intermedios, productos terminados, repuestos, etc.

Demanda (D): La cantidad de productos que los clientes solicitan. La demanda puede ser determinística (conocida y constante) o aleatoria (incertidumbre sobre la cantidad solicitada y su tiempo).

Lead Time (LT): El tiempo que transcurre desde que se realiza una orden hasta que se recibe el inventario.

Costo de mantenimiento (H): Los costos asociados con mantener productos en inventario, como costos de almacenamiento, deterioro, seguros, etc.

Costo de pedido (S): Es el costo que incurre una empresa cada vez que realiza un pedido. Esto incluye costos de transporte, preparación, procesamiento, etc.

Costo de escasez (B): Es el costo que se produce cuando no hay suficiente inventario para satisfacer la demanda, lo que puede generar pérdida de ventas o de clientes.

Costo de adquisición (C): El precio de compra de los productos que se agregan al inventario.

Punto de Reorden (R): Nivel crítico de inventario que indica el momento en que se debe realizar un nuevo pedido al proveedor. Asegurando que el nuevo lote llegue antes de que el stock actual se agote.

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

Punto de Reorden (R)
R = d * LT

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