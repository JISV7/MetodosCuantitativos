import sys
import copy
from collections import deque

def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    
    # Procesar encabezados
    encabezados = lineas[0].strip().split('\t')
    destinos = encabezados[:-1]  # Excluir el primer elemento (vacío) y el último (Oft)
    
    origenes = []
    ofertas = []
    costos = []
    
    # Procesar filas de orígenes
    for i in range(1, len(lineas) - 1):
        datos = lineas[i].strip().split('\t')
        origenes.append(datos[0])
        fila_costos = [float(x) for x in datos[1:-1]]
        costos.append(fila_costos)
        ofertas.append(float(datos[-1]))
    
    # Procesar última fila (demandas)
    demanda_linea = lineas[-1].strip().split('\t')
    demandas = [float(x) for x in demanda_linea[1:1+len(destinos)]]
    
    return origenes, destinos, costos, ofertas, demandas

def balancear(origenes, destinos, costos, ofertas, demandas):
    total_ofertas = sum(ofertas)
    total_demandas = sum(demandas)
    
    if total_ofertas == total_demandas:
        return origenes, destinos, costos, ofertas, demandas
    
    if total_ofertas < total_demandas:
        origenes.append('Ficticio')
        costos.append([0] * len(destinos))
        ofertas.append(total_demandas - total_ofertas)
    else:
        destinos.append('Ficticio')
        for fila in costos:
            fila.append(0)
        demandas.append(total_ofertas - total_demandas)
    return origenes, destinos, costos, ofertas, demandas

def esquina_noroeste(costos, ofertas, demandas):
    m = len(ofertas)
    n = len(demandas)
    asignaciones = [[0] * n for _ in range(m)]
    ofertas_rest = ofertas.copy()
    demandas_rest = demandas.copy()
    
    i, j = 0, 0
    while i < m and j < n:
        if ofertas_rest[i] <= 0:
            i += 1
            continue
        if demandas_rest[j] <= 0:
            j += 1
            continue
            
        cantidad = min(ofertas_rest[i], demandas_rest[j])
        asignaciones[i][j] = cantidad
        ofertas_rest[i] -= cantidad
        demandas_rest[j] -= cantidad
        
        if ofertas_rest[i] == 0:
            i += 1
        if demandas_rest[j] == 0:
            j += 1
    
    # Calcular costo total
    total = 0
    for i in range(m):
        for j in range(n):
            total += asignaciones[i][j] * costos[i][j]
    return total, asignaciones

def costo_minimo(costos, ofertas, demandas):
    m = len(ofertas)
    n = len(demandas)
    asignaciones = [[0] * n for _ in range(m)]
    ofertas_rest = ofertas.copy()
    demandas_rest = demandas.copy()
    
    while sum(ofertas_rest) > 0 and sum(demandas_rest) > 0:
        # Encontrar la celda con menor costo
        min_costo = float('inf')
        i_min, j_min = -1, -1
        
        for i in range(m):
            for j in range(n):
                if ofertas_rest[i] > 0 and demandas_rest[j] > 0 and costos[i][j] < min_costo:
                    min_costo = costos[i][j]
                    i_min, j_min = i, j
        
        if i_min == -1:
            break
            
        cantidad = min(ofertas_rest[i_min], demandas_rest[j_min])
        asignaciones[i_min][j_min] += cantidad
        ofertas_rest[i_min] -= cantidad
        demandas_rest[j_min] -= cantidad
    
    # Calcular costo total
    total = 0
    for i in range(m):
        for j in range(n):
            total += asignaciones[i][j] * costos[i][j]
    return total, asignaciones

def vogel(costos, ofertas, demandas):
    m = len(ofertas)
    n = len(demandas)
    asignaciones = [[0] * n for _ in range(m)]
    ofertas_rest = ofertas.copy()
    demandas_rest = demandas.copy()
    
    while sum(ofertas_rest) > 0 and sum(demandas_rest) > 0:
        # Calcular penalizaciones para filas y columnas
        penalizaciones_filas = [0] * m
        penalizaciones_columnas = [0] * n
        
        # Para filas
        for i in range(m):
            if ofertas_rest[i] <= 0:
                penalizaciones_filas[i] = -1
                continue
                
            costos_disponibles = []
            for j in range(n):
                if demandas_rest[j] > 0:
                    costos_disponibles.append(costos[i][j])
            
            if len(costos_disponibles) == 0:
                penalizaciones_filas[i] = -1
            else:
                costos_disponibles.sort()
                if len(costos_disponibles) >= 2:
                    penalizaciones_filas[i] = costos_disponibles[1] - costos_disponibles[0]
                else:
                    penalizaciones_filas[i] = 0
        
        # Para columnas
        for j in range(n):
            if demandas_rest[j] <= 0:
                penalizaciones_columnas[j] = -1
                continue
                
            costos_disponibles = []
            for i in range(m):
                if ofertas_rest[i] > 0:
                    costos_disponibles.append(costos[i][j])
            
            if len(costos_disponibles) == 0:
                penalizaciones_columnas[j] = -1
            else:
                costos_disponibles.sort()
                if len(costos_disponibles) >= 2:
                    penalizaciones_columnas[j] = costos_disponibles[1] - costos_disponibles[0]
                else:
                    penalizaciones_columnas[j] = 0
        
        # Encontrar máxima penalización
        max_penalizacion = -float('inf')
        tipo = None  # 'fila' o 'columna'
        idx = -1
        
        for i in range(m):
            if penalizaciones_filas[i] > max_penalizacion:
                max_penalizacion = penalizaciones_filas[i]
                tipo = 'fila'
                idx = i
        
        for j in range(n):
            if penalizaciones_columnas[j] > max_penalizacion:
                max_penalizacion = penalizaciones_columnas[j]
                tipo = 'columna'
                idx = j
        
        if max_penalizacion == -float('inf'):
            break
            
        # Encontrar celda con menor costo en la fila o columna seleccionada
        min_costo = float('inf')
        i_sel, j_sel = -1, -1
        
        if tipo == 'fila':
            i = idx
            for j in range(n):
                if demandas_rest[j] > 0 and ofertas_rest[i] > 0 and costos[i][j] < min_costo:
                    min_costo = costos[i][j]
                    i_sel, j_sel = i, j
        else:  # tipo == 'columna'
            j = idx
            for i in range(m):
                if ofertas_rest[i] > 0 and demandas_rest[j] > 0 and costos[i][j] < min_costo:
                    min_costo = costos[i][j]
                    i_sel, j_sel = i, j
        
        if i_sel == -1 or j_sel == -1:
            break
            
        cantidad = min(ofertas_rest[i_sel], demandas_rest[j_sel])
        asignaciones[i_sel][j_sel] += cantidad
        ofertas_rest[i_sel] -= cantidad
        demandas_rest[j_sel] -= cantidad
    
    # Calcular costo total
    total = 0
    for i in range(m):
        for j in range(n):
            total += asignaciones[i][j] * costos[i][j]
    return total, asignaciones

def encontrar_ciclo(asignaciones, start_i, start_j):
    m = len(asignaciones)
    n = len(asignaciones[0])
    # Usaremos un DFS que alterna entre filas y columnas
    path = []
    visited = set()
    
    def dfs(i, j, depth, from_row):
        # Agregamos la celda actual al camino
        path.append((i, j))
        visited.add((i, j))
        
        # Si hemos vuelto al inicio y tenemos al menos 4 celdas, retornamos
        if depth >= 4 and (i, j) == (start_i, start_j):
            return True
        
        # Alternamos entre buscar en filas y columnas
        if from_row:
            # Buscar en la misma columna j
            for ni in range(m):
                if ni == i: continue
                # Ignorar celdas vacías excepto la de inicio
                if asignaciones[ni][j] > 0 or (ni == start_i and j == start_j):
                    if (ni, j) in visited and (ni, j) != (start_i, start_j):
                        continue
                    if dfs(ni, j, depth + 1, False):
                        return True
        else:
            # Buscar en la misma fila i
            for nj in range(n):
                if nj == j: continue
                # Ignorar celdas vacías excepto la de inicio
                if asignaciones[i][nj] > 0 or (i == start_i and nj == start_j):
                    if (i, nj) in visited and (i, nj) != (start_i, start_j):
                        continue
                    if dfs(i, nj, depth + 1, True):
                        return True
        
        # Backtracking
        path.pop()
        visited.remove((i, j))
        return False
    
    # Iniciar búsqueda alternando
    if dfs(start_i, start_j, 1, True) or dfs(start_i, start_j, 1, False):
        return path
    return None

def modi(costos, ofertas, demandas, asignaciones_iniciales):
    m = len(ofertas)
    n = len(demandas)
    asignaciones = copy.deepcopy(asignaciones_iniciales)
    
    # Identificar celdas básicas iniciales
    basicas = []
    for i in range(m):
        for j in range(n):
            if asignaciones[i][j] > 0:
                basicas.append((i, j))
    
    # Asegurar solución básica (m + n - 1 celdas básicas)
    required = m + n - 1
    if len(basicas) < required:
        # Agregar celdas degeneradas usando un enfoque de conexión
        parent = list(range(m + n))
        rank = [0] * (m + n)
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            rx = find(x)
            ry = find(y)
            if rx == ry:
                return False
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[ry] = rx
                rank[rx] += 1
            return True
        
        # Conectar celdas básicas existentes
        for (i, j) in basicas:
            x = i
            y = j + m
            if find(x) != find(y):
                union(x, y)
        
        # Agregar celdas que conecten componentes
        non_basicas = [(i, j) for i in range(m) for j in range(n) if (i, j) not in basicas]
        needed = required - len(basicas)
        added = 0
        
        for cell in non_basicas[:]:
            if added >= needed:
                break
            i, j = cell
            x = i
            y = j + m
            if find(x) != find(y):
                if union(x, y):
                    basicas.append(cell)
                    asignaciones[i][j] = 0
                    added += 1
        
        # Agregar celdas restantes si es necesario
        while added < needed and non_basicas:
            cell = non_basicas.pop(0)
            i, j = cell
            basicas.append(cell)
            asignaciones[i][j] = 0
            added += 1

    iter_count = 0
    max_iter = 1000
    
    while iter_count < max_iter:
        iter_count += 1
        
        # Paso 1: Calcular multiplicadores
        u = [0.0] * m
        v = [0.0] * n
        calculated_u = [False] * m
        calculated_v = [False] * n
        
        # Fijar u[0] = 0 y propagar
        calculated_u[0] = True
        queue = deque([(0, 'row')])
        
        while queue:
            idx, tipo = queue.popleft()
            if tipo == 'row':
                i = idx
                for j in range(n):
                    if (i, j) in basicas and not calculated_v[j]:
                        v[j] = costos[i][j] - u[i]
                        calculated_v[j] = True
                        queue.append((j, 'col'))
            else:
                j = idx
                for i in range(m):
                    if (i, j) in basicas and not calculated_u[i]:
                        u[i] = costos[i][j] - v[j]
                        calculated_u[i] = True
                        queue.append((i, 'row'))
        
        # Paso 2: Calcular costos marginales
        min_negative = 0
        min_i, min_j = -1, -1
        
        for i in range(m):
            for j in range(n):
                if (i, j) in basicas:
                    continue
                d_ij = costos[i][j] - (u[i] + v[j])
                if d_ij < min_negative:
                    min_negative = d_ij
                    min_i, min_j = i, j
        
        # Si no hay costos negativos, solución óptima
        if min_negative >= 0:
            break
        
        # Paso 3: Encontrar ciclo
        ciclo = encontrar_ciclo(asignaciones, min_i, min_j)
        if ciclo is None:
            break
        
        # Paso 4: Asignar signos alternados
        signos = {}
        for idx, (i, j) in enumerate(ciclo):
            signos[(i, j)] = '+' if idx % 2 == 0 else '-'
        
        # Paso 5: Calcular theta
        theta = float('inf')
        leaving = None
        for (i, j), sign in signos.items():
            if sign == '-' and asignaciones[i][j] < theta:
                theta = asignaciones[i][j]
                leaving = (i, j)
        
        # Paso 6: Ajustar valores
        for (i, j), sign in signos.items():
            if sign == '+':
                asignaciones[i][j] += theta
            else:
                asignaciones[i][j] -= theta
        
        # Actualizar celdas básicas
        if (min_i, min_j) not in basicas:
            basicas.append((min_i, min_j))
        if leaving and asignaciones[leaving[0]][leaving[1]] == 0:
            if leaving in basicas:
                basicas.remove(leaving)
    
    # Calcular costo total
    total = 0
    for i in range(m):
        for j in range(n):
            total += asignaciones[i][j] * costos[i][j]
    
    return total, asignaciones

def menu():
    archivo = sys.argv[1]
    try:
        origenes, destinos, costos, ofertas, demandas = leer_archivo(archivo)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
    
    # Balancear el problema si es necesario
    origenes, destinos, costos, ofertas, demandas = balancear(origenes, destinos, costos, ofertas, demandas)
    
    print("Seleccione el método:")
    print("1. Esquina Noroeste")
    print("2. Costo Mínimo")
    print("3. Vogel")
    print("4. MODI (Vogel)")
    opcion = input("Ingrese el número correspondiente: ")
    
    if opcion == '1':
        resultado, asignaciones = esquina_noroeste(costos, ofertas, demandas)
        metodo = "Esquina Noroeste"
    elif opcion == '2':
        resultado, asignaciones = costo_minimo(costos, ofertas, demandas)
        metodo = "Costo Mínimo"
    elif opcion == '3':
        resultado, asignaciones = vogel(costos, ofertas, demandas)
        metodo = "Vogel"
    elif opcion == '4':
        _, asignaciones_vogel = vogel(costos, ofertas, demandas)
        resultado, asignaciones = modi(costos, ofertas, demandas, asignaciones_vogel)
        metodo = "MODI (Vogel)"
    else:
        print("\033[91mOpción inválida\033[0m")
        return
    
    # Imprimir detalles de asignaciones
    print(f"\nResolviendo por \033[93m{metodo}\033[0m el resultado es:\n")
    
    total_verificacion = 0
    for i in range(len(origenes)):
        for j in range(len(destinos)):
            if asignaciones[i][j] > 0:
                origen = origenes[i]
                destino = destinos[j]
                unidades = asignaciones[i][j]
                costo_unit = costos[i][j]
                subtotal = unidades * costo_unit
                total_verificacion += subtotal
                print(f"{origen} --> {destino} | {unidades} * {costo_unit} = {subtotal}")
    
    print(f"\nCosto total = \033[93m{total_verificacion}\033[0m\n\n")

def main():
    if len(sys.argv) != 2:
        print("Forma de uso: python transporte.py <archivo_de_datos>")
        return
    while True:
        menu()

if __name__ == "__main__":
    main()