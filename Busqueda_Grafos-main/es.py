"""
    Acosta Avila Diego Ernesto
    Diaz Pompa Jesus Eduardo
    Ruiz Alejandro Ignacio Alberto
"""

from utilGrafo import obtener_distancia, generar_tabla_pasos, generar_tabla_pasos_secuencial

def es_horario(grafo, nodo_inicio, nodo_final):
    """
    Algoritmo de Escalada Simple en sentido horario.
    Evalúa primero los vecinos en orden al JSON y selecciona el primer 
    vecino que mejore la heurística h(n) hacia nodo_final.
    Firma estricta: (grafo, nodo_inicio, nodo_final).
    """
    inicio = int(nodo_inicio)
    fin = int(nodo_final)
    # Lista de nodos generados en orden secuencial para la tabla ASCII
    # Cada elemento es un dict: {"nodo": int, "visitado": 0|1|None, "antecesor": int, "costo": int}
    historial_pasos = []
    
    # Costo heurístico del nodo de origen
    costo_inicio = obtener_distancia(inicio, fin)
    
    # Registramos el nodo inicial (visitado=0, antecesor=0)
    historial_pasos.append({
        "nodo": inicio,
        "visitado": 0,
        "antecesor": 0,
        "costo": costo_inicio
    })

    nodo_actual = inicio
    costo_actual = costo_inicio
    encontrado = False

    while True:
        # El nodo en el que estamos parados pasa a ser visitado (1)
        # Buscamos la última ocurrencia del nodo actual para marcarlo
        for estado in reversed(historial_pasos):
            if estado["nodo"] == nodo_actual and estado["visitado"] != 1:
                estado["visitado"] = 1
                break

        if nodo_actual == fin:
            encontrado = True
            break

        vecinos_dict = grafo.get(nodo_actual, {})
        vecinos_horarios = list(vecinos_dict.keys())

        hubo_mejora = False

        # Evaluamos y agregamos un vecino a la vez
        for vecino in vecinos_horarios:
            costo_vecino = obtener_distancia(vecino, fin)

            # Agregamos el vecino al historial en el instante exacto en que se genera
            nuevo_estado = {
                "nodo": vecino,
                "visitado": None,  # Queda sin marcar por ahora
                "antecesor": nodo_actual,
                "costo": costo_vecino
            }
            historial_pasos.append(nuevo_estado)

            # Si el vecino MEJORA la heurística actual (costo menor)
            if costo_vecino < costo_actual:
                nodo_actual = vecino
                costo_actual = costo_vecino
                hubo_mejora = True
                # Interrumpimos la evaluación de los demás vecinos de este nodo
                break

        # Si ninguno de los vecinos de 'nodo_actual' mejoró el costo, caemos en un máximo local
        if not hubo_mejora:
            break

    # Reconstrucción de la ruta desde el destino/último nodo hacia el inicio
    ruta = []
    curr = nodo_actual
    
    # Para reconstruir el camino correcto cuando hay nodos repetidos,
    # rastreamos los antecesores desde el último estado registrado hacia atrás
    idx_rastreo = len(historial_pasos) - 1
    while curr != 0 and idx_rastreo >= 0:
        estado = historial_pasos[idx_rastreo]
        if estado["nodo"] == curr:
            ruta.append(curr)
            curr = estado["antecesor"]
        idx_rastreo -= 1

    ruta.reverse()

    # Formateo de la tabla de pasos ASCII
    pasos_tabla = generar_tabla_pasos_secuencial(historial_pasos)

    return ruta, pasos_tabla

def es_antihorario(grafo, nodo_inicio, nodo_final):
    """
    Algoritmo de Escalada Simple en sentido antihorario.
    Evalúa primero los vecinos en orden inverso al JSON y selecciona el primer 
    vecino que mejore la heurística h(n) hacia nodo_final.
    Firma estricta: (grafo, nodo_inicio, nodo_final).
    """
    inicio = int(nodo_inicio)
    fin = int(nodo_final)

    historial_pasos = []
    costo_inicio = obtener_distancia(inicio, fin)
    
    historial_pasos.append({
        "nodo": inicio,
        "visitado": 0,
        "antecesor": 0,
        "costo": costo_inicio
    })

    nodo_actual = inicio
    costo_actual = costo_inicio
    encontrado = False

    while True:
        for estado in reversed(historial_pasos):
            if estado["nodo"] == nodo_actual and estado["visitado"] != 1:
                estado["visitado"] = 1
                break

        if nodo_actual == fin:
            encontrado = True
            break

        # Obtenemos los vecinos e invertimos el orden para la exploración antihoraria
        vecinos_dict = grafo.get(nodo_actual, {})
        vecinos_antihorarios = list(reversed(list(vecinos_dict.keys())))

        hubo_mejora = False

        # Evaluamos y agregamos un vecino a la vez en sentido antihorario
        for vecino in vecinos_antihorarios:
            costo_vecino = obtener_distancia(vecino, fin)

            historial_pasos.append({
                "nodo": vecino,
                "visitado": None,
                "antecesor": nodo_actual,
                "costo": costo_vecino
            })

            if costo_vecino < costo_actual:
                nodo_actual = vecino
                costo_actual = costo_vecino
                hubo_mejora = True
                break

        if not hubo_mejora:
            break

    # Reconstrucción de la ruta
    ruta = []
    curr = nodo_actual
    idx_rastreo = len(historial_pasos) - 1
    while curr != 0 and idx_rastreo >= 0:
        estado = historial_pasos[idx_rastreo]
        if estado["nodo"] == curr:
            ruta.append(curr)
            curr = estado["antecesor"]
        idx_rastreo -= 1

    ruta.reverse()

    pasos_tabla = generar_tabla_pasos_secuencial(historial_pasos)

    return ruta, pasos_tabla