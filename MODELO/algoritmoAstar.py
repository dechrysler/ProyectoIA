def algoritmo_Astar_bidireccional(G, inicial, final, heuristica, coords, considerar_minusvalidos=False):
    
    # Ejecutar A* en dirección normal (inicial → final)
    ruta_directa, tiempo_directo, transbordos_directo = algoritmo_Astar(
        G, inicial, final, heuristica, coords, considerar_minusvalidos
    )
    
    # Ejecutar A* en dirección inversa (final → inicial)
    ruta_inversa, tiempo_inverso, transbordos_inverso = algoritmo_Astar(
        G, final, inicial, heuristica, coords, considerar_minusvalidos
    )
    
    # Invertir la ruta inversa para que sea de inicial → final
    if ruta_inversa:
        ruta_inversa_corregida = list(reversed(ruta_inversa))
    else:
        ruta_inversa_corregida = []
    
    # Seleccionar la mejor ruta basada en el tiempo
    if not ruta_directa and not ruta_inversa_corregida:
        return [], 0.0, 0
    
    if not ruta_directa:
        return ruta_inversa_corregida, tiempo_inverso, transbordos_inverso
    
    if not ruta_inversa_corregida:
        return ruta_directa, tiempo_directo, transbordos_directo
    
    # Ambas rutas existen, seleccionar la de menor tiempo
    if tiempo_directo <= tiempo_inverso:
        return ruta_directa, tiempo_directo, transbordos_directo
    else:
        return ruta_inversa_corregida, tiempo_inverso, transbordos_inverso


def algoritmo_Astar(G, inicial, final, heuristica, coords, considerar_minusvalidos=False):
   

    # ----- PARÁMETROS -----
    PENALIZACION_TRANSBORDO_MIN = 2      # minutos extra por transbordo "molesto"
    PENALIZACION_NO_ACCESIBLE_MIN = 9999 # usado sólo si modo accesibilidad exige evitar no accesibles
    VELOCIDAD_TREN_KMH = 35              # km/h
    TIEMPO_TRANSBORDO_MIN = 5            # tiempo real promedio de transbordo en min
    TIEMPO_ESPERA_ESTACION_MIN = 0.5     # espera en cada estación (min)

    def metros_a_minutos(dist_m):
        """Convierte metros a minutos según VELOCIDAD_TREN_KMH"""
        return (dist_m / 1000.0) / VELOCIDAD_TREN_KMH * 60.0

    # conjuntos y diccionarios
    abiertos = set([inicial])
    cerrados = set()
    padres = {}
    g_score = {inicial: 0.0}            # coste real (minutos) desde inicial
    tiempo_acumulado = {inicial: 0.0}   # alias de g_score, por claridad
    f_score = {inicial: metros_a_minutos(heuristica(G, inicial, final, coords))}  # g + h (min)

    lineas_usadas = {inicial: None}
    transbordos = {inicial: 0}
    es_transbordo_ruta = {inicial: False}

    while abiertos:
        # nodo con menor f
        actual = min(abiertos, key=lambda n: f_score.get(n, float('inf')))

        if actual == final:
            break

        abiertos.remove(actual)
        cerrados.add(actual)

        for vecino in G.neighbors(actual):
            if vecino in cerrados:
                continue

            # líneas en nodo actual y vecino
            lineas_actual = G.nodes[actual].get('lineas', [])
            lineas_vecino = G.nodes[vecino].get('lineas', [])
            lineas_comunes = list(set(lineas_actual) & set(lineas_vecino))
            if not lineas_comunes:
                # si no comparten línea no hay conexión "normal"
                continue

            # decidir si hay cambio de línea
            if lineas_usadas.get(actual) is None:
                cambio = False
                linea_propuesta = lineas_comunes[0]
            else:
                linea_base = lineas_usadas.get(actual)
                if linea_base in lineas_vecino:
                    cambio = False
                    linea_propuesta = linea_base
                else:
                    cambio = True
                    linea_propuesta = lineas_comunes[0]

            if considerar_minusvalidos:
                # Si hay transbordo y la estación no es accesible, rechazar
                if cambio and not G.nodes[vecino].get('accesible', False):
                    continue
                # Si no hay transbordo, permitir incluso si no es accesible (estación intermedia)

            # coste (en minutos) de moverse actual->vecino
            dist_m = G.edges[actual, vecino].get('peso', 0.0)
            tiempo_viaje_min = metros_a_minutos(dist_m)
            tiempo_espera = TIEMPO_ESPERA_ESTACION_MIN
            tiempo_extra = 0.0
            if cambio:
                tiempo_extra += TIEMPO_TRANSBORDO_MIN + PENALIZACION_TRANSBORDO_MIN

            # Penalización adicional para transbordos no accesibles (solo en modo normal)
            if not considerar_minusvalidos and cambio and not G.nodes[vecino].get('accesible', False):
                tiempo_extra += PENALIZACION_TRANSBORDO_MIN * 2  # Penalización doble

            candidato_g = g_score[actual] + tiempo_viaje_min + tiempo_espera + tiempo_extra

            # si encontramos mejor camino al vecino
            if vecino not in g_score or candidato_g < g_score[vecino]:
                padres[vecino] = actual
                g_score[vecino] = candidato_g
                tiempo_acumulado[vecino] = candidato_g
                transbordos[vecino] = transbordos.get(actual, 0) + (1 if cambio else 0)
                lineas_usadas[vecino] = linea_propuesta
                es_transbordo_ruta[vecino] = cambio

                # heurística: convertir metros->minutos antes de sumar
                h_metros = heuristica(G, vecino, final, coords)
                h_minutos = metros_a_minutos(h_metros) if (h_metros is not None and h_metros != float('inf')) else float('inf')
                f_score[vecino] = g_score[vecino] + h_minutos

                abiertos.add(vecino)

    # Reconstrucción de ruta
    ruta = []
    if final in padres or inicial == final:
        nodo = final
        ruta.append(nodo)
        while nodo in padres:
            nodo = padres[nodo]
            ruta.append(nodo)
        ruta.reverse()
        tiempo_total = tiempo_acumulado.get(final, 0.0)
        num_trans = transbordos.get(final, 0)
        return ruta, tiempo_total, num_trans
    else:
        # No se encontró ruta: devolver ruta vacía para que SistemaMetro lance la excepción
        return [], 0.0, 0
