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
    
    # Nodos
    for nodo in datos.keys():
        nodo_id = int(nodo)
        pos = posiciones.get(nodo_id, {"x": 0, "y": 0})
        elements.append({
            "data": {"id": str(nodo_id), "label": str(nodo_id)},
            "position": pos
        })
    
    # Aristas (procesar pares para evitar duplicar líneas)
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

def generar_tabla_pasos(orden_nodos, registro, heurísticas=None):
    """
    Genera la representación visual en tabla ASCII basada en el historial de búsqueda.
    Si se pasa el diccionario 'heurísticas' {nodo: costo}, agrega la fila 'Costo a fin' (h(n)).
    """
    filas_datos = []
    
    for nodo in orden_nodos:
        vis = str(registro[nodo]["visitado"]) if registro[nodo]["visitado"] is not None else ""
        ant = str(registro[nodo]["antecesor"])
        costo = str(heurísticas[nodo]) if (heurísticas and nodo in heurísticas) else ""
        filas_datos.append((str(nodo), vis, ant, costo))

    # Cálculo dinámico de anchos por columna
    anchos = [
        max(len(n), len(v), len(a), len(c)) + 2 
        for n, v, a, c in filas_datos
    ]
    
    label_nodo = " Nodo "
    label_vis  = " Visitado "
    label_ant  = " Antecesor "
    label_cost = " Costo "

    # Construcción de líneas
    linea_nodo = " | ".join(f"{n:^{w}}" for (n, _, _, _), w in zip(filas_datos, anchos))
    linea_vis  = " | ".join(f"{v:^{w}}" for (_, v, _, _), w in zip(filas_datos, anchos))
    linea_ant  = " | ".join(f"{a:^{w}}" for (_, _, a, _), w in zip(filas_datos, anchos))
    linea_cost = " | ".join(f"{c:^{w}}" for (_, _, _, c), w in zip(filas_datos, anchos))

    separador = "-" * (len(label_cost) + len(linea_cost) + 12)

    tabla = [
        separador,
        f"| {label_nodo:<12} | {linea_nodo} |",
        f"| {label_vis:<12} | {linea_vis} |",
        f"| {label_ant:<12} | {linea_ant} |"
    ]

    # Si hay costos/heurísticas disponibles, agregamos la fila a la tabla
    if heurísticas:
        tabla.append(f"| {label_cost:<12} | {linea_cost} |")

    tabla.append(separador)
    
    return "\n".join(tabla)

def generar_tabla_pasos_secuencial(historial_pasos):
    filas_datos = []
    
    for estado in historial_pasos:
        nodo_str = str(estado["nodo"])
        vis_str = str(estado["visitado"]) if estado["visitado"] is not None else ""
        ant_str = str(estado["antecesor"])
        costo_str = str(estado["costo"])
        filas_datos.append((nodo_str, vis_str, ant_str, costo_str))

    # Anchos dinámicos por columna
    anchos = [
        max(len(n), len(v), len(a), len(c)) + 2 
        for n, v, a, c in filas_datos
    ]
    
    label_nodo = " Nodo "
    label_vis  = " Visitado "
    label_ant  = " Antecesor "
    label_cost = " Costo "

    linea_nodo = " | ".join(f"{n:^{w}}" for (n, _, _, _), w in zip(filas_datos, anchos))
    linea_vis  = " | ".join(f"{v:^{w}}" for (_, v, _, _), w in zip(filas_datos, anchos))
    linea_ant  = " | ".join(f"{a:^{w}}" for (_, _, a, _), w in zip(filas_datos, anchos))
    linea_cost = " | ".join(f"{c:^{w}}" for (_, _, _, c), w in zip(filas_datos, anchos))

    separador = "-" * (len(label_cost) + len(linea_cost) + 12)

    tabla = [
        separador,
        f"| {label_nodo:<12} | {linea_nodo} |",
        f"| {label_vis:<12} | {linea_vis} |",
        f"| {label_ant:<12} | {linea_ant} |",
        f"| {label_cost:<12} | {linea_cost} |",
        separador
    ]
    
    return "\n".join(tabla)

DISTANCIAS_RAW = [
    [0],
    [908, 0],
    [117, 515, 0],
    [687, 448, 886, 0],
    [1651, 970, 1373, 922, 0],
    [117, 791, 999, 804, 1540, 0],
    [1882, 1013, 117, 1404, 1191, 1765, 0],
    [1310, 441, 844, 832, 529, 1193, 662, 0],
    [889, 246, 684, 202, 720, 840, 1202, 630, 0],
    [760, 181, 559, 479, 997, 643, 1194, 622, 277, 0],
    [2348, 1707, 1811, 1619, 697, 2237, 694, 1223, 1417, 1694, 0],
    [782, 127, 541, 426, 943, 665, 1140, 568, 223, 54, 1640, 0],
    [697, 546, 984, 98, 952, 814, 1502, 930, 300, 577, 1649, 523, 0],
    [1370, 928, 317, 1319, 1463, 1253, 1154, 934, 1117, 774, 1848, 756, 1417, 0],
    [1431, 750, 1153, 702, 220, 1320, 971, 309, 500, 777, 917, 723, 732, 1250, 0],
    [395, 513, 721, 744, 1262, 278, 1407, 915, 542, 365, 1959, 387, 842, 975, 1042, 0],
    [697, 316, 739, 504, 1022, 580, 1329, 757, 302, 180, 1719, 202, 602, 954, 802, 302, 0],
    [1328, 600, 291, 991, 1148, 1211, 826, 606, 789, 729, 1520, 711, 1089, 328, 928, 933, 913, 0],
    [490, 540, 626, 817, 1335, 373, 1553, 981, 615, 392, 2032, 414, 915, 890, 1115, 95, 397, 960, 0],
    [481, 636, 813, 867, 1385, 364, 1610, 1038, 665, 480, 2082, 510, 965, 1077, 1165, 123, 425, 1056, 187, 0],
    [1244, 511, 300, 902, 1046, 1127, 737, 517, 700, 664, 1431, 646, 1000, 417, 826, 849, 844, 89, 895, 972, 0],
    [810, 171, 344, 542, 1029, 693, 1072, 500, 340, 215, 1766, 197, 640, 559, 809, 416, 395, 514, 446, 538, 449, 0],
    [881, 572, 235, 943, 1430, 764, 1352, 901, 741, 616, 2046, 598, 1041, 499, 1210, 486, 796, 526, 391, 578, 615, 401, 0],
    [1145, 460, 898, 416, 506, 1034, 1257, 595, 214, 491, 1203, 437, 446, 1331, 286, 756, 516, 1003, 829, 879, 914, 554, 955, 0],
    [513, 631, 780, 862, 1380, 396, 1605, 1033, 660, 483, 2077, 505, 960, 1044, 1160, 118, 420, 1051, 154, 33, 967, 533, 545, 874, 0],
    [461, 497, 704, 678, 1195, 344, 1432, 938, 476, 349, 1893, 371, 776, 1041, 976, 66, 236, 898, 161, 189, 852, 360, 552, 690, 184, 0],
    [1407, 538, 642, 929, 784, 1290, 475, 255, 727, 719, 1169, 665, 1027, 679, 564, 1012, 854, 351, 1043, 1135, 262, 597, 877, 850, 1130, 957, 0],
    [1000, 131, 534, 522, 839, 883, 882, 310, 320, 312, 1576, 258, 620, 797, 619, 605, 447, 469, 636, 728, 380, 190, 591, 534, 723, 550, 407, 0]
]

def obtener_distancia(nodo_a, nodo_b):
    """
    Obtiene la distancia entre dos nodos (1 a 28)
    consultando la pirámide triangular.
    """
    idx_a = nodo_a - 1
    idx_b = nodo_b - 1
    
    # Aseguramos que el índice mayor vaya primero
    fil = max(idx_a, idx_b)
    col = min(idx_a, idx_b)
    
    return DISTANCIAS_RAW[fil][col]

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