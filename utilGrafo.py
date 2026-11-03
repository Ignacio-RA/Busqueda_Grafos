import json

def cargar_grafo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        datos = json.load(archivo)
    
    grafo_limpio = {}
    
    # Recorremos el diccionario para convertir todo a enteros (int)
    for nodo_origen, vecinos in datos.items():
        origen_int = int(nodo_origen)
        grafo_limpio[origen_int] = {}
        
        for nodo_destino, peso in vecinos.items():
            destino_int = int(nodo_destino)
            grafo_limpio[origen_int][destino_int] = peso
            
    return grafo_limpio

def cargar_grafo_cytoscape(nombre_archivo, posiciones):
    with open(nombre_archivo, 'r') as archivo:
        datos = json.load(archivo)
    
    elements = []
    
    # 1. Nodos
    for nodo in datos.keys():
        nodo_id = int(nodo)
        pos = posiciones.get(nodo_id, {"x": 0, "y": 0})
        elements.append({
            "data": {"id": str(nodo_id), "label": str(nodo_id)},
            "position": pos
        })
    
    # 2. Aristas (procesar pares para evitar duplicar líneas)
    pares_procesados = set()
    
    for origen, vecinos in datos.items():
        u = str(origen)
        for destino, peso in vecinos.items():
            v = str(destino)
            
            # Identificador único del par sin importar el orden
            par_key = tuple(sorted([int(u), int(v)]))
            if par_key in pares_procesados:
                continue
            
            pares_procesados.add(par_key)
            
            # Comprobar si existe la dirección opuesta en el JSON
            es_bidireccional = v in datos and u in datos[v]
            
            elements.append({
                "data": {
                    "id": f"{u}-{v}",
                    "source": u,
                    "target": v,
                    "weight": peso,
                    "bidirectional": es_bidireccional
                }
            })
            
    return elements

def generar_tabla_pasos(orden_nodos, registro):
    """
    Genera la representación visual en tabla ASCII basada en el historial de búsqueda.
    """
    filas_datos = []
    for nodo in orden_nodos:
        vis = str(registro[nodo]["visitado"]) if registro[nodo]["visitado"] is not None else ""
        ant = str(registro[nodo]["antecesor"])
        filas_datos.append((str(nodo), vis, ant))

    # Cálculo dinámico del ancho de cada columna
    anchos = [
        max(len(n), len(v), len(a)) + 2 
        for n, v, a in filas_datos
    ]
    
    label_nodo = " Nodo "
    label_vis = " Visitado "
    label_ant = " Antecesor "

    linea_nodo = " | ".join(f"{n:^{w}}" for (n, _, _), w in zip(filas_datos, anchos))
    linea_vis  = " | ".join(f"{v:^{w}}" for (_, v, _), w in zip(filas_datos, anchos))
    linea_ant  = " | ".join(f"{a:^{w}}" for (_, _, a), w in zip(filas_datos, anchos))

    separador = "-" * (len(label_ant) + len(linea_ant) + 6)

    tabla = [
        separador,
        f"| {label_nodo:<11} | {linea_nodo} |",
        f"| {label_vis:<11} | {linea_vis} |",
        f"| {label_ant:<11} | {linea_ant} |",
        separador
    ]
    
    return "\n".join(tabla)

# Posiciones de los nodos para la visualización en el frontend
POSICIONES_NODOS = {
    1:  {"x": 830, "y": 980},
    2:  {"x": 620, "y": 550},
    3:  {"x": 870, "y": 380},
    4:  {"x": 570, "y": 800},
    5:  {"x": 230, "y": 350},
    6:  {"x": 830, "y": 900},
    7:  {"x": 420, "y": 70},
    8:  {"x": 440, "y": 430},
    9:  {"x": 560, "y": 690},
    10: {"x": 760, "y": 590},
    11: {"x": 30,  "y": 30},
    12: {"x": 680, "y": 590},
    13: {"x": 490, "y": 830},
    14: {"x": 970, "y": 200},
    15: {"x": 340, "y": 490},
    16: {"x": 880, "y": 790},
    17: {"x": 710, "y": 750},
    18: {"x": 810, "y": 200},
    19: {"x": 910, "y": 720},
    20: {"x": 950, "y": 840},
    21: {"x": 720, "y": 250},
    22: {"x": 720, "y": 490},
    23: {"x": 950, "y": 550},
    24: {"x": 450, "y": 620},
    25: {"x": 960, "y": 780},
    26: {"x": 800, "y": 790},
    27: {"x": 570, "y": 300},
    28: {"x": 580, "y": 460}
}