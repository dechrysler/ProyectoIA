import sys
import os

# Añadir la carpeta Data al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Data'))

from coordenadas import haversine

def heuristica_distancia_directa(G, actual, destino, coords):
  
    if actual not in coords or destino not in coords:
        return float('inf')  #  Si no hay coordenadas, retorna infinito
    
    # Obtener coordenadas de la estación actual y del destino
    lat_actual, lon_actual = coords[actual]
    lat_destino, lon_destino = coords[destino]
    
    # Calcular distancia directa entre actual y destino
    distancia = haversine(lat_actual, lon_actual, lat_destino, lon_destino)
    
    return distancia

# Mantener compatibilidad con el nombre original si es necesario
def heuristica_distancia_centro(G, actual, destino, coords):

    return heuristica_distancia_directa(G, actual, destino, coords)
