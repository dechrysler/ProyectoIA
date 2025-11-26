class ControladorMetro:
    def __init__(self):
        from MODELO.sistema_metro import SistemaMetro
        self.modelo = SistemaMetro()
        self.vista = None
        self.considerar_minusvalidos = False
    
    def set_vista(self, vista):
        self.vista = vista
    
    def calcular_ruta(self, origen, destino):
        try:
            ruta, tiempo_total, num_transbordos = self.modelo.calcular_ruta(origen, destino, self.considerar_minusvalidos)
            if self.vista:
                self.vista.mostrar_ruta(ruta, tiempo_total, num_transbordos, self.considerar_minusvalidos)
            return ruta
        except Exception as e:
            if self.vista:
                self.vista.mostrar_error(str(e))
            return None

    def calcular_tiempo_aproximado(self, origen, destino):
        """Calcula y retorna el tiempo aproximado entre dos estaciones"""
        if origen and destino:
            tiempo, distancia = self.modelo.calcular_tiempo_aproximado(origen, destino)
            return tiempo, distancia
        return 0, 0
    
    def toggle_minusvalidos(self, estado):
        self.considerar_minusvalidos = estado
        print(f"♿ Modo accesibilidad: {'ACTIVADO' if estado else 'DESACTIVADO'}")
    
    def obtener_estaciones(self):
        return self.modelo.obtener_estaciones()
    
    def obtener_info_estacion(self, estacion):
        return self.modelo.obtener_info_estacion(estacion)
    
    def limpiar_ruta(self):
        self.modelo.ruta_actual = []
        if self.vista:
            self.vista.limpiar_ruta()
    
    def obtener_tiempo_ruta(self):
        return self.modelo.obtener_tiempo_ruta()
    
    def obtener_transbordos_ruta(self):
        return self.modelo.obtener_transbordos_ruta()
    
    def es_estacion_accesible(self, estacion):
        return self.modelo.es_estacion_accesible(estacion)
    
    def obtener_estaciones_accesibles(self):
        return self.modelo.obtener_estaciones_accesibles()
    
    def obtener_estaciones_no_accesibles(self):
        return self.modelo.obtener_estaciones_no_accesibles()