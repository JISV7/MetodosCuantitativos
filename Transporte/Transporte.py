import sys

def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    
    # Procesar encabezados
    encabezados = lineas[0].strip().split('\t')
    destinos = encabezados[1:-1]  # Excluir el primer elemento (vacío) y el último (Oft)
    
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
    return total

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
    return total

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
    return total

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
    opcion = input("Ingrese el número correspondiente: ")
    
    if opcion == '1':
        resultado = esquina_noroeste(costos, ofertas, demandas)
        metodo = "Esquina Noroeste"
    elif opcion == '2':
        resultado = costo_minimo(costos, ofertas, demandas)
        metodo = "Costo Mínimo"
    elif opcion == '3':
        resultado = vogel(costos, ofertas, demandas)
        metodo = "Vogel"
    else:
        #print("Opción inválida")
        print("\033[91mOpción inválida\033[0m")
        return
    
    #print(f"Resolviendo por {metodo} el resultado es:")
    print(f"Resolviendo por \033[93m{metodo}\033[0m el resultado es:")
    print(f"Costo total = \033[93m{float(resultado)}\033[0m\n\n")

def main():
    if len(sys.argv) != 2:
        print("Forma de uso: python transporte.py <archivo_de_datos>")
        return
    while True:
        menu()

if __name__ == "__main__":
    main()