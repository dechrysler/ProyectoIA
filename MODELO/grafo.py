import networkx as nx
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Data'))

from estaciones import estaciones, aristas, accesibilidad_estaciones
from coordenadas import haversine

def crear_grafo(coordenadas):
    G = nx.Graph()

    for nombre, lineas in estaciones:
        # Obtener accesibilidad (True si es accesible, False si no)
        accesible = accesibilidad_estaciones.get(nombre, False)
        G.add_node(nombre, lineas=lineas, accesible=accesible)

    for a, b in aristas:
        if a in coordenadas and b in coordenadas:
            lat1, lon1 = coordenadas[a]
            lat2, lon2 = coordenadas[b]
            distancia = haversine(lat1, lon1, lat2, lon2)
            G.add_edge(a, b, peso=distancia)
        else:
            print(f"⚠️ No se encontraron coordenadas para: {a} o {b}")

    return G