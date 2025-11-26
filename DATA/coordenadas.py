import csv
import os
from math import radians, sin, cos, asin, sqrt

def cargar_coordenadas_desde_csv(nombre_archivo="coordenadas_estaciones.csv"):
    """Carga las coordenadas desde un archivo CSV"""
    coordenadas = {}
    
    posibles_rutas = [
        nombre_archivo,
        os.path.join("DATA", nombre_archivo),
        os.path.join(os.path.dirname(__file__), nombre_archivo),
        os.path.join(os.path.dirname(__file__), "..", "DATA", nombre_archivo),
        os.path.join(os.path.dirname(__file__), "..", nombre_archivo),
    ]
    
    archivo_encontrado = None
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            archivo_encontrado = ruta
            print(f"✅ Encontrado archivo CSV en: {ruta}")
            break
    
    if not archivo_encontrado:
        print("❌ No se pudo encontrar el archivo CSV en las siguientes ubicaciones:")
        for ruta in posibles_rutas:
            print(f"   - {ruta}")
        raise FileNotFoundError(f"No se encontró el archivo {nombre_archivo}")
    
    try:
        with open(archivo_encontrado, 'r', encoding='utf-8') as archivo_csv:
            reader = csv.reader(archivo_csv)
            header = next(reader)
            print(f"📋 Cabecera del CSV: {header}")
            
            estaciones_cargadas = 0
            for fila in reader:
                if len(fila) == 3:
                    estacion, lat, lon = fila
                    coordenadas[estacion] = (float(lat), float(lon))
                    estaciones_cargadas += 1
        
        print(f"✅ Se cargaron {estaciones_cargadas} estaciones desde el CSV")
        return coordenadas
        
    except Exception as e:
        print(f"❌ Error leyendo el archivo CSV: {e}")
        raise

def haversine(lat1, lon1, lat2, lon2): 
    """Calcula la distancia entre dos puntos geográficos usando la fórmula Haversine"""
    R = 6371000  # Radio de la Tierra en metros
    lon1_radianes = radians(lon1)
    lat1_radianes = radians(lat1)
    lon2_radianes = radians(lon2)
    lat2_radianes = radians(lat2)
    
    dif_lat = lat2_radianes - lat1_radianes
    dif_lon = lon2_radianes - lon1_radianes
    
    a = sin(dif_lat/2)**2 + cos(lat1_radianes) * cos(lat2_radianes) * sin(dif_lon/2)**2
    c = 2 * asin(sqrt(a))
    
    return R * c

def calcular_distancia_recta(estacion1, estacion2, coordenadas):
    """Calcula la distancia en línea recta entre dos estaciones"""
    if estacion1 not in coordenadas or estacion2 not in coordenadas:
        return float('inf')
    
    lat1, lon1 = coordenadas[estacion1]
    lat2, lon2 = coordenadas[estacion2]
    
    return haversine(lat1, lon1, lat2, lon2)

def calcular_tiempo_aproximado(distancia_metros, velocidad_kmh=30):
    """
    Calcula el tiempo aproximado en minutos para una distancia dada
    Velocidad promedio considerando: tren + caminar + esperas
    """
    # Convertir distancia a kilómetros
    distancia_km = distancia_metros / 1000
    
    # Tiempo en horas = distancia / velocidad
    tiempo_horas = distancia_km / velocidad_kmh
    
    # Convertir a minutos
    tiempo_minutos = tiempo_horas * 60
    
    # Añadir tiempo fijo por transbordos aproximados (2 minutos por transbordo estimado)
    transbordos_estimados = max(1, distancia_km / 3)  # Estimación: 1 transbordo cada 3km
    tiempo_transbordos = transbordos_estimados * 2
    
    tiempo_total = tiempo_minutos + tiempo_transbordos
    
    return tiempo_total

# Función con nombre compatible para no romper el código existente
def obtener_coordenadas():
    """Función principal para obtener coordenadas (solo carga del CSV)"""
    return cargar_coordenadas_desde_csv()

if __name__ == "__main__":
    try:
        coordenadas = obtener_coordenadas()
        print(f"✅ Coordenadas cargadas exitosamente - Total: {len(coordenadas)}")
        
        # Ejemplo de cálculo
        if 'Tacubaya' in coordenadas and 'Centro Medico' in coordenadas:
            distancia = calcular_distancia_recta('Tacubaya', 'Centro Medico', coordenadas)
            tiempo = calcular_tiempo_aproximado(distancia)
            print(f"📏 Tacubaya → Centro Médico: {distancia/1000:.2f} km, ⏱️ {tiempo:.1f} min")
            
    except Exception as e:
        print(f"❌ Error: {e}")