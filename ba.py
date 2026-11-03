from collections import deque
from utilGrafo import generar_tabla_pasos

def ba_horario(grafo, nodo_inicio, nodo_final):
    """
    Búsqueda en Anchura (sentido horario).
    Firma estricta: (grafo, nodo_inicio, nodo_final)
    """
    inicio = int(nodo_inicio)
    fin = int(nodo_final)

    registro = {}
    orden_nodos = []

    # Marcamos el nodo de origen
    registro[inicio] = {"visitado": 0, "antecesor": 0}
    orden_nodos.append(inicio)
    
    cola = deque([inicio])
    encontrado = False
    
    while cola:
        nodo_actual = cola.popleft()
        registro[nodo_actual]["visitado"] = 1
        
        if nodo_actual == fin:
            encontrado = True
            break
            
        vecinos_dict = grafo.get(nodo_actual, {})
        
        for vecino in vecinos_dict.keys():
            if vecino not in registro:
                registro[vecino] = {
                    "visitado": None,
                    "antecesor": nodo_actual
                }
                orden_nodos.append(vecino)
                cola.append(vecino)

    # Reconstrucción de la ruta
    ruta = []
    if encontrado:
        curr = fin
        while curr != 0:
            ruta.append(curr)
            curr = registro[curr]["antecesor"]
        ruta.reverse()
    else:
        ruta = None

    pasos_tabla = generar_tabla_pasos(orden_nodos, registro)
    
    return ruta, pasos_tabla

def ba_antihorario(grafo, nodo_inicio, nodo_final):
    """
    Búsqueda en Anchura en sentido antihorario.
    Invierte el orden de exploración de los vecinos del JSON.
    Firma estricta: (grafo, nodo_inicio, nodo_final)
    """
    # Normalización de nodos a int para coherencia en las comparaciones
    inicio = int(nodo_inicio)
    fin = int(nodo_final)

    registro = {}
    orden_nodos = []
    
    # Marcamos el nodo de origen
    registro[inicio] = {"visitado": 0, "antecesor": 0}
    orden_nodos.append(inicio)
    
    cola = deque([inicio])
    encontrado = False
    
    while cola:
        nodo_actual = cola.popleft()
        registro[nodo_actual]["visitado"] = 1
        
        if nodo_actual == fin:
            encontrado = True
            break
            
        # Obtenemos las llaves del nodo y las invertimos para el sentido antihorario
        vecinos_dict = grafo.get(nodo_actual, {})
        vecinos_antihorarios = reversed(list(vecinos_dict.keys()))
        
        for vecino_raw in vecinos_antihorarios:
            vecino = int(vecino_raw)
            if vecino not in registro:
                registro[vecino] = {
                    "visitado": None,  # Permanece sin marcar (vacío en tabla) hasta procesarse
                    "antecesor": nodo_actual
                }
                orden_nodos.append(vecino)
                cola.append(vecino)

    # Reconstrucción de la ruta encontrada
    ruta = []
    if encontrado:
        curr = fin
        while curr != 0:
            ruta.append(curr)
            curr = registro[curr]["antecesor"]
        ruta.reverse()
    else:
        ruta = None

    # Formateo de la tabla de pasos ASCII
    pasos_tabla = generar_tabla_pasos(orden_nodos, registro)
    
    return ruta, pasos_tabla