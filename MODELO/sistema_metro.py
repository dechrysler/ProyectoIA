import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'DATA'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from MODELO.grafo import crear_grafo
from DATA.coordenadas import obtener_coordenadas, calcular_distancia_recta, calcular_tiempo_aproximado
from MODELO.algoritmoAstar import algoritmo_Astar_bidireccional, algoritmo_Astar
from MODELO.heuristicas import heuristica_distancia_directa

class SistemaMetro:
    def __init__(self):
        print("🔄 Inicializando sistema metro...")
        self.coordenadas = obtener_coordenadas()
        print("✅ Coordenadas cargadas")
        self.grafo = crear_grafo(self.coordenadas)
        print("✅ Grafo creado")
        self.ruta_actual = []
        self.tiempo_actual = 0
        self.transbordos_actual = 0
    
    def calcular_ruta(self, origen, destino, considerar_minusvalidos=False):
        """Calcula la ruta entre dos estaciones usando búsqueda bidireccional"""
        print(f"🔄 Calculando ruta de {origen} a {destino} (Minusválidos: {considerar_minusvalidos})")
        
        if origen not in self.grafo.nodes:
            raise ValueError(f"Estación de origen '{origen}' no encontrada")
        if destino not in self.grafo.nodes:
            raise ValueError(f"Estación de destino '{destino}' no encontrada")
        
        # Verificar accesibilidad de origen y destino si el modo está activado
        if considerar_minusvalidos:
            if not self.grafo.nodes[origen].get('accesible', False):
                raise ValueError(f"Estación de origen '{origen}' no es accesible para personas con discapacidad")
            if not self.grafo.nodes[destino].get('accesible', False):
                raise ValueError(f"Estación de destino '{destino}' no es accesible para personas con discapacidad")
        
        # 🔄 USAR BÚSQUEDA BIDIRECCIONAL MEJORADA
        ruta, tiempo_total, num_transbordos = algoritmo_Astar_bidireccional(
            self.grafo, origen, destino, 
            heuristica_distancia_directa,
            self.coordenadas,
            considerar_minusvalidos
        )
        
        # Verificar si se encontró una ruta
        if not ruta or ruta[0] != origen:
            if considerar_minusvalidos:
                raise ValueError("No se pudo encontrar una ruta accesible entre las estaciones seleccionadas")
            else:
                raise ValueError("No se pudo encontrar una ruta entre las estaciones seleccionadas")
        
        # Guardar información
        self.ruta_actual = ruta
        self.tiempo_actual = tiempo_total
        self.transbordos_actual = num_transbordos
        
        print(f"✅ Ruta calculada: {ruta}")
        print(f"⏱️ Tiempo estimado: {tiempo_total:.1f} minutos")
        print(f"🔄 Transbordos: {num_transbordos}")
        print(f"♿ Modo accesibilidad: {'ACTIVADO' if considerar_minusvalidos else 'DESACTIVADO'}")
        
        return ruta, tiempo_total, num_transbordos

    def calcular_tiempo_aproximado(self, origen, destino):
        """Calcula el tiempo aproximado en línea recta entre dos estaciones"""
        if origen not in self.coordenadas or destino not in self.coordenadas:
            return 0, 0
        
        distancia = calcular_distancia_recta(origen, destino, self.coordenadas)
        tiempo_aproximado = calcular_tiempo_aproximado(distancia)
        
        return tiempo_aproximado, distancia

    def obtener_tiempo_ruta(self):
        return getattr(self, 'tiempo_actual', 0)

    def obtener_transbordos_ruta(self):
        return getattr(self, 'transbordos_actual', 0)
    
    def obtener_estaciones(self):
        return list(self.grafo.nodes())
    
    def obtener_info_estacion(self, estacion):
        if estacion in self.grafo.nodes:
            return {
                'lineas': self.grafo.nodes[estacion].get('lineas', []),
                'coordenadas': self.coordenadas.get(estacion, (0, 0)),
                'es_transbordo': len(self.grafo.nodes[estacion].get('lineas', [])) > 1,
                'accesible': self.grafo.nodes[estacion].get('accesible', False)
            }
        return None

    def es_estacion_accesible(self, estacion):
        if estacion in self.grafo.nodes:
            return self.grafo.nodes[estacion].get('accesible', False)
        return False
    
    def obtener_estaciones_accesibles(self):
        return [estacion for estacion in self.grafo.nodes if self.grafo.nodes[estacion].get('accesible', False)]
    
    def obtener_estaciones_no_accesibles(self):
        return [estacion for estacion in self.grafo.nodes if not self.grafo.nodes[estacion].get('accesible', False)]