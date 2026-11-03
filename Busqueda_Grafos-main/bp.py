"""
    Acosta Avila Diego Ernesto
    Diaz Pompa Jesus Eduardo
    Ruiz Alejandro Ignacio Alberto
"""

from utilGrafo import generar_tabla_pasos

def bp_horario(grafo, nodo_inicio, nodo_final):
    """
    Búsqueda en Profundidad (BP) en sentido horario.
    Firma estricta: (grafo, nodo_inicio, nodo_final)
    """
    # Normalizamos los nodos a tipo entero
    inicio = int(nodo_inicio)
    fin = int(nodo_final)

    # Estructuras de control para rastreo y construcción de la tabla
    registro = {}     # Registra {nodo: {"visitado": 0|1, "antecesor": int}}
    orden_nodos = []  # Mantiene la secuencia de descubrimiento de los nodos
    
    # El nodo inicial se descubre primero (visitado=0, antecesor=0)
    registro[inicio] = {"visitado": 0, "antecesor": 0}
    orden_nodos.append(inicio)

    # En BP usamos una PILA (LIFO) en lugar de una Cola (FIFO)
    pila = [inicio]
    encontrado = False

    # Iteración principal del algoritmo
    while pila:
        # Extraemos el último nodo ingresado (comportamiento LIFO)
        nodo_actual = pila.pop()

        # Si el nodo ya fue expandido anteriormente, lo ignoramos para evitar ciclos
        if registro[nodo_actual]["visitado"] == 1:
            continue

        # Marcamos el nodo actual como visitado (1) al momento de procesarlo
        registro[nodo_actual]["visitado"] = 1

        # Comprobamos si alcanzamos el nodo objetivo
        if nodo_actual == fin:
            encontrado = True
            break

        # Para expandir los vecinos en orden HORARIO en una Pila (LIFO):
        # Debemos apilarlos en orden INVERSO a como queremos procesarlos.
        # Al apilarlos al revés, el primer vecino original quedará hasta arriba de la pila.
        vecinos_dict = grafo.get(nodo_actual, {})
        vecinos_horarios = list(vecinos_dict.keys())
        vecinos_para_pila = reversed(vecinos_horarios)

        # Exploración e inserción a la pila
        for vecino in vecinos_para_pila:
            # Si el vecino no ha sido registrado previamente en la búsqueda
            if vecino not in registro:
                registro[vecino] = {
                    "visitado": None,  # Permanece sin visitar hasta ser desapilado
                    "antecesor": nodo_actual
                }
                orden_nodos.append(vecino)
                pila.append(vecino)
            elif registro[vecino]["visitado"] is None:
                # Si ya estaba en la pila pero no visitado, actualizamos su antecesor al camino más reciente
                registro[vecino]["antecesor"] = nodo_actual
                pila.append(vecino)

    # Reconstrucción del camino solución desde el final hasta el inicio
    ruta = []
    if encontrado:
        curr = fin
        while curr != 0:
            ruta.append(curr)
            curr = registro[curr]["antecesor"]
        ruta.reverse()
    else:
        ruta = None

    # Formateo de la tabla de pasos ASCII mediante tu función auxiliar
    pasos_tabla = generar_tabla_pasos(orden_nodos, registro)

    return ruta, pasos_tabla

def bp_antihorario(grafo, nodo_inicio, nodo_final):
    """
    Búsqueda en Profundidad (BP) en sentido antihorario.
    Firma estricta: (grafo, nodo_inicio, nodo_final)
    """
    # Normalizamos los nodos a tipo entero
    inicio = int(nodo_inicio)
    fin = int(nodo_final)

    # Estructuras de control para rastreo y construcción de la tabla
    registro = {}     # Registra {nodo: {"visitado": 0|1, "antecesor": int}}
    orden_nodos = []  # Mantiene la secuencia de descubrimiento de los nodos
    
    # El nodo inicial se descubre primero (visitado=0, antecesor=0)
    registro[inicio] = {"visitado": 0, "antecesor": 0}
    orden_nodos.append(inicio)

    # Inicializamos la pila (LIFO) con el nodo de origen
    pila = [inicio]
    encontrado = False

    # Iteración principal del algoritmo
    while pila:
        # Extraemos el último nodo ingresado
        nodo_actual = pila.pop()

        # Si el nodo ya fue expandido anteriormente, omitimos
        if registro[nodo_actual]["visitado"] == 1:
            continue

        # Marcamos como visitado (1)
        registro[nodo_actual]["visitado"] = 1

        # Comprobamos si alcanzamos el objetivo
        if nodo_actual == fin:
            encontrado = True
            break

        # Para expandir vecinos en orden ANTIHORARIO en una Pila (LIFO):
        # Tomamos la lista original y la dejamos tal cual (SIN invertir antes de apilar).
        # De esta forma, el último vecino en sentido horario (el primero en antihorario) 
        # queda hasta arriba de la pila para extraerse de inmediato.
        vecinos_dict = grafo.get(nodo_actual, {})
        vecinos_antihorarios = list(vecinos_dict.keys())  # Mantiene el orden natural para que LIFO invierta

        # Exploración e inserción a la pila
        for vecino in vecinos_antihorarios:
            if vecino not in registro:
                registro[vecino] = {
                    "visitado": None,  # Pendiente de visitar
                    "antecesor": nodo_actual
                }
                orden_nodos.append(vecino)
                pila.append(vecino)
            elif registro[vecino]["visitado"] is None:
                # Si ya estaba en la pila pero no visitado, actualizamos su antecesor
                registro[vecino]["antecesor"] = nodo_actual
                pila.append(vecino)

    # Reconstrucción del camino solución
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