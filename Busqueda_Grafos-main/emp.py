"""
    Acosta Avila Diego Ernesto
    Diaz Pompa Jesus Eduardo
    Ruiz Alejandro Ignacio Alberto
"""

from utilGrafo import obtener_distancia, generar_tabla_pasos_secuencial


def _escalada_maxima_pendiente(grafo, nodo_inicio, nodo_final, invertir):
    """Evalúa todos los vecinos y avanza al de menor h si mejora estrictamente.

    Devuelve el recorrido alcanzado y la tabla, incluso si se detiene en un
    mínimo local o una meseta sin alcanzar el destino. No hace retroceso.
    Los empates se resuelven por el orden de exploración de los vecinos.
    """
    # Convertimos los identificadores a enteros, como las claves del grafo cargado.
    inicio = int(nodo_inicio)
    fin = int(nodo_final)
    # Guardamos el recorrido directamente: solo agregamos el vecino elegido.
    ruta = [inicio]
    # Cada estado representa una aparición de un nodo en la tabla.
    # "costo" es h(n): la distancia estimada al destino; no suma pesos de aristas.
    # Antecesor 0 indica que el nodo inicial no tiene padre.
    estado_actual = {
        "nodo": inicio,
        "visitado": None,
        "antecesor": 0,
        "costo": obtener_distancia(inicio, fin),
    }
    # El historial incluye vecinos evaluados aunque nunca se llegue a visitarlos.
    # Un nodo puede aparecer varias veces si es vecino de distintos nodos.
    historial = [estado_actual]

    while True:
        # Solo marcamos con 1 el estado al que realmente avanzó la búsqueda.
        # Los vecinos evaluados pero no elegidos permanecen con None (celda vacía).
        estado_actual["visitado"] = 1
        nodo_actual = estado_actual["nodo"]
        # Si llegamos al destino, terminamos sin generar más vecinos.
        if nodo_actual == fin:
            break

        # Horario conserva el orden del JSON; antihorario lo invierte.
        vecinos = list(grafo.get(nodo_actual, {}))
        if invertir:
            vecinos.reverse()

        # A diferencia de escalada simple, evaluamos TODOS los vecinos antes
        # de elegir: buscamos el menor h(n), no la primera mejora encontrada.
        mejor_estado = None
        for vecino in vecinos:
            estado = {
                "nodo": vecino,
                "visitado": None,
                "antecesor": nodo_actual,
                "costo": obtener_distancia(vecino, fin),
            }
            # Registrar un vecino no significa que ya haya sido visitado.
            historial.append(estado)
            # Usamos < para conservar al primer vecino en caso de empate.
            if mejor_estado is None or estado["costo"] < mejor_estado["costo"]:
                mejor_estado = estado

        # Nos detenemos si no hay vecinos o ninguno mejora estrictamente h(n).
        # Esto incluye mínimos locales y mesetas: no retrocedemos ni aceptamos
        # pasos de igual o mayor heurística. No se garantiza llegar al destino.
        if mejor_estado is None or mejor_estado["costo"] >= estado_actual["costo"]:
            break

        # Avanzamos al mejor vecino. Es el mismo diccionario del historial,
        # por lo que al marcarlo en la próxima vuelta también cambia la tabla.
        estado_actual = mejor_estado
        ruta.append(estado_actual["nodo"])

    # Devolvemos el recorrido alcanzado (puede ser parcial) y la tabla con
    # las filas Nodo, Visitado, Antecesor y Costo heurístico.
    return ruta, generar_tabla_pasos_secuencial(historial)


def emp_horario(grafo, nodo_inicio, nodo_final):
    """Escalada de máxima pendiente; desempata en el orden del JSON."""
    # False mantiene el orden original para evaluar y resolver empates.
    return _escalada_maxima_pendiente(grafo, nodo_inicio, nodo_final, False)


def emp_antihorario(grafo, nodo_inicio, nodo_final):
    """Escalada de máxima pendiente; desempata en el orden inverso del JSON."""
    # True invierte el orden; el criterio de elegir el menor h(n) es el mismo.
    return _escalada_maxima_pendiente(grafo, nodo_inicio, nodo_final, True)
