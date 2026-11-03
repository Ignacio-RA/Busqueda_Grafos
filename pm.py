from utilGrafo import obtener_distancia, generar_tabla_pasos_secuencial

def pm_horario(grafo, nodo_inicio, nodo_final):
    """
    Algoritmo Primero el Mejor según la teoría de f' = g + h' (A*).
    Sentido Horario.
    Firma estricta: (grafo, nodo_inicio, nodo_final).
    """
    inicio = int(nodo_inicio)
    fin = int(nodo_final)

    # Comenzar con ABIERTOS conteniendo sólo el estado inicial
    # Guardaremos diccionarios para rastrear g, h', f' y padre
    h_inicio = obtener_distancia(inicio, fin)
    
    # {nodo: {"g": int, "h": int, "f": int, "padre": int, "visitado": 0|1|None}}
    nodos_info = {
        inicio: {
            "g": 0,
            "h": h_inicio,
            "f": 0 + h_inicio,
            "padre": 0,
            "visitado": 0
        }
    }

    # ABIERTOS guarda la lista de nodos pendientes por evaluar
    abiertos = [inicio]
    
    # Para mantener el registro secuencial exacto de impresiones en la tabla
    historial_pasos = [{
        "nodo": inicio,
        "visitado": 0,
        "antecesor": 0,
        "costo": nodos_info[inicio]["f"]
    }]

    encontrado = False

    # Hasta que se llegue a un objetivo o no queden nodos en ABIERTOS hacer:
    while abiertos:
        # Tomar el mejor nodo de ABIERTOS (el que tiene menor f')
        abiertos.sort(key=lambda n: nodos_info[n]["f"])
        nodo_actual = abiertos.pop(0)

        # Marcar visitado (1)
        nodos_info[nodo_actual]["visitado"] = 1
        for h in reversed(historial_pasos):
            if h["nodo"] == nodo_actual and h["visitado"] != 1:
                h["visitado"] = 1
                break

        # Si alcanzamos el objetivo, terminamos
        if nodo_actual == fin:
            encontrado = True
            break

        # Generar sus sucesores en orden horario
        vecinos_dict = grafo.get(nodo_actual, {})
        vecinos_horarios = list(vecinos_dict.keys())

        # Para cada sucesor hacer:
        for vecino in vecinos_horarios:
            peso_arista = vecinos_dict[vecino]
            nuevo_g = nodos_info[nodo_actual]["g"] + peso_arista
            h_vecino = obtener_distancia(vecino, fin)
            nuevo_f = nuevo_g + h_vecino

            # Caso A: "Si no se ha generado con anterioridad..."
            if vecino not in nodos_info:
                nodos_info[vecino] = {
                    "g": nuevo_g,
                    "h": h_vecino,
                    "f": nuevo_f,
                    "padre": nodo_actual,
                    "visitado": None
                }
                abiertos.append(vecino)
                
                historial_pasos.append({
                    "nodo": vecino,
                    "visitado": None,
                    "antecesor": nodo_actual,
                    "costo": nuevo_f  # Se muestra el valor f' = g + h'
                })

            # Caso B: "Si ya se ha generado antes, cambiar al padre si el nuevo camino es mejor..."
            elif nuevo_g < nodos_info[vecino]["g"]:
                # Se actualiza el costo empleado y el padre
                nodos_info[vecino]["g"] = nuevo_g
                nodos_info[vecino]["f"] = nuevo_f
                nodos_info[vecino]["padre"] = nodo_actual

                # Si no estaba en ABIERTOS (ya había sido visitado), se vuelve a reabrir para reevaluar sucesores
                if vecino not in abiertos:
                    abiertos.append(vecino)
                    nodos_info[vecino]["visitado"] = None

                historial_pasos.append({
                    "nodo": vecino,
                    "visitado": None,
                    "antecesor": nodo_actual,
                    "costo": nuevo_f
                })

    # Reconstrucción del camino óptimo final
    ruta = []
    if encontrado:
        curr = fin
        while curr != 0:
            ruta.append(curr)
            curr = nodos_info[curr]["padre"]
        ruta.reverse()
    else:
        ruta = None

    pasos_tabla = generar_tabla_pasos_secuencial(historial_pasos)

    return ruta, pasos_tabla

def pm_antihorario(grafo, nodo_inicio, nodo_final):
    """
    Algoritmo Primero el Mejor según la teoría de f' = g + h'.
    Sentido Antihorario.
    Firma estricta: (grafo, nodo_inicio, nodo_final).
    """
    inicio = int(nodo_inicio)
    fin = int(nodo_final)

    h_inicio = obtener_distancia(inicio, fin)
    
    nodos_info = {
        inicio: {
            "g": 0,
            "h": h_inicio,
            "f": 0 + h_inicio,
            "padre": 0,
            "visitado": 0
        }
    }

    abiertos = [inicio]
    
    historial_pasos = [{
        "nodo": inicio,
        "visitado": 0,
        "antecesor": 0,
        "costo": nodos_info[inicio]["f"]
    }]

    encontrado = False

    while abiertos:
        # Tomar el nodo con menor f' de ABIERTOS.
        abiertos.sort(key=lambda n: nodos_info[n]["f"])
        nodo_actual = abiertos.pop(0)

        nodos_info[nodo_actual]["visitado"] = 1
        for h in reversed(historial_pasos):
            if h["nodo"] == nodo_actual and h["visitado"] != 1:
                h["visitado"] = 1
                break

        if nodo_actual == fin:
            encontrado = True
            break

        # Sucesores en sentido ANTIHORARIO
        vecinos_dict = grafo.get(nodo_actual, {})
        vecinos_antihorarios = list(reversed(list(vecinos_dict.keys())))

        for vecino in vecinos_antihorarios:
            peso_arista = vecinos_dict[vecino]
            nuevo_g = nodos_info[nodo_actual]["g"] + peso_arista
            h_vecino = obtener_distancia(vecino, fin)
            nuevo_f = nuevo_g + h_vecino

            # Si no se ha generado previamente
            if vecino not in nodos_info:
                nodos_info[vecino] = {
                    "g": nuevo_g,
                    "h": h_vecino,
                    "f": nuevo_f,
                    "padre": nodo_actual,
                    "visitado": None
                }
                abiertos.append(vecino)
                
                historial_pasos.append({
                    "nodo": vecino,
                    "visitado": None,
                    "antecesor": nodo_actual,
                    "costo": nuevo_f
                })

            # Si ya fue generado y el nuevo camino mejora g
            elif nuevo_g < nodos_info[vecino]["g"]:
                nodos_info[vecino]["g"] = nuevo_g
                nodos_info[vecino]["f"] = nuevo_f
                nodos_info[vecino]["padre"] = nodo_actual

                if vecino not in abiertos:
                    abiertos.append(vecino)
                    nodos_info[vecino]["visitado"] = None

                historial_pasos.append({
                    "nodo": vecino,
                    "visitado": None,
                    "antecesor": nodo_actual,
                    "costo": nuevo_f
                })

    ruta = []
    if encontrado:
        curr = fin
        while curr != 0:
            ruta.append(curr)
            curr = nodos_info[curr]["padre"]
        ruta.reverse()
    else:
        ruta = None

    pasos_tabla = generar_tabla_pasos_secuencial(historial_pasos)

    return ruta, pasos_tabla