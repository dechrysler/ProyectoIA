import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InterfazMetro:
    def __init__(self, controlador):
        self.controlador = controlador
        self.controlador.set_vista(self)

        self.origen_seleccionado = None
        self.destino_seleccionado = None
        self.marcadores_estaciones = {}
        self.linea_ruta = None
        self.modo_minusvalidos = False

        # ===============================
        # Datos de líneas, colores y coordenadas
        # ===============================
        self.secuencias_lineas = {
            "L1": ["Observatorio","Tacubaya","Juanacatlan","Chapultepec","Sevilla","Insurgentes","Cuauhtemoc","Balderas"],
            "L3": ["Juarez","Balderas","Niños Heroes","Hospital General","Centro Medico","Etiopía","Eugenia","Division del Norte","Zapata","Coyoacan","Viveros","M. A. De Quevedo","Copilco","Universidad"],
            "L7": ["Polanco","Auditorio","Constituyentes","Tacubaya","San Pedro de los Pinos","San Antonio","Mixcoac","Barranca del Muerto"],
            "L9": ["Tacubaya","Patriotismo","Chilpancingo","Centro Medico","Lazaro Cardenas"],
            "L12": ["Mixcoac","Insurgentes Sur","Hospital 20 de Noviembre","Zapata","Parque de los Venados","Eje Central"]
        }
        self.COLORES = {"L1":"#e91e63","L3":"#7a9a01","L7":"#f28c28","L9":"#4e2a1e","L12":"#9b59b6"}
        self.coordenadas_linea = {
            "L1": {"Observatorio": (-6,1.5), "Tacubaya": (-5,1.5), "Juanacatlan": (-3,1.5), "Chapultepec": (-1,1.5),
                   "Sevilla": (0.7,1.5), "Insurgentes": (2.5,1.5), "Cuauhtemoc": (4.5,1.5), "Balderas": (5.5,1.5)},
            "L3": {"Juarez": (5.5,4), "Balderas": (5.5,1.5), "Niños Heroes": (5.5,0), "Hospital General": (5.5,-1),
                   "Centro Medico": (5.5,-2), "Etiopía": (5.5,-3), "Eugenia": (5.5,-4), "Division del Norte": (5.5,-5),
                   "Zapata": (5.5,-6), "Coyoacan": (5.5,-7), "Viveros": (5.5,-8), "M. A. De Quevedo": (5.5,-9),
                   "Copilco": (5.5,-10), "Universidad": (5.5,-11)},
            "L7": {"Polanco": (-5,5), "Auditorio": (-5,3.5), "Constituyentes": (-5,2.5), "Tacubaya": (-5,1.5),
                   "San Pedro de los Pinos": (-5,0), "San Antonio": (-5,-1.5), "Mixcoac": (-5,-3), "Barranca del Muerto": (-5,-4.5)},
            "L9": {"Tacubaya": (-5,1.5), "Patriotismo": (-1,0), "Chilpancingo": (1.5,-1), "Centro Medico": (5.5,-2), "Lazaro Cardenas": (8,-3)},
            "L12": {"Mixcoac": (-5,-3), "Insurgentes Sur": (-1,-4), "Hospital 20 de Noviembre": (2,-5),
                    "Zapata": (5.5,-6), "Parque de los Venados": (7,-7), "Eje Central": (8.5,-8)}
        }
        self.coordenadas = {k:v for d in self.coordenadas_linea.values() for k,v in d.items()}

        self.desplazamientos = {s:(0.3,0,'left',9) for s in self.secuencias_lineas["L7"]}
        self.desplazamientos.update({s:(-0.3,0,'right',9) for s in self.secuencias_lineas["L3"] if s not in ["Balderas","Zapata"]})
        self.desplazamientos.update({s:(0,0.3,'center',9) for s in ["Observatorio","Juanacatlan","Chapultepec","Sevilla","Insurgentes","Cuauhtemoc","Patriotismo","Chilpancingo","Centro Medico","Lazaro Cardenas","Insurgentes Sur","Hospital 20 de Noviembre","Parque de los Venados","Eje Central"]})
        self.desplazamientos.update({"Tacubaya": (0,-0.4,'center',9), "Balderas": (0,-0.4,'center',9), "Zapata": (0,-0.4,'center',9)})

        self.inicializar_interfaz()

    # --------------------- Inicialización ---------------------
    def inicializar_interfaz(self):
        self.crear_ventana_principal()
        self.crear_barra_lateral()
        self.crear_mapa()
        self.fig.canvas.mpl_connect('button_press_event', self.al_hacer_clic)

    def crear_etiqueta(self, texto, tam=14, negrita=False):
        f = ("Arial", tam, "bold") if negrita else ("Arial", tam)
        return tk.Label(self.marco_izquierdo, text=texto, font=f, bg="#f0f0f0")

    def crear_boton(self, texto, comando, color_fondo="#f0f0f0", color_texto="black"):
        return tk.Button(self.marco_izquierdo, text=texto, font=("Arial",14,"bold"), bg=color_fondo, fg=color_texto, command=comando)

    def crear_ventana_principal(self):
        self.raiz = tk.Tk()
        self.raiz.title("Mapa del Metro CDMX - MVC")
        ancho_pantalla, alto_pantalla = self.raiz.winfo_screenwidth(), self.raiz.winfo_screenheight()
        ancho, alto = int(ancho_pantalla*0.8), int(alto_pantalla*0.8)
        self.raiz.geometry(f"{ancho}x{alto}+{(ancho_pantalla-ancho)//2}+{(alto_pantalla-alto)//2}")

    def crear_barra_lateral(self):
        self.marco_izquierdo = tk.Frame(self.raiz, width=300, bg="#f0f0f0")
        self.marco_izquierdo.pack(side="left", fill="y", padx=10, pady=10)

        self.crear_etiqueta("Mapa del Metro CDMX", 24, True).pack(pady=30)
        self.crear_etiqueta("Estación Origen:").pack(anchor="w", pady=5)
        self.entrada_origen = tk.Entry(self.marco_izquierdo, width=30, font=("Arial",14)); self.entrada_origen.pack(pady=5)
        self.crear_etiqueta("Estación Destino:").pack(anchor="w", pady=5)
        self.entrada_destino = tk.Entry(self.marco_izquierdo, width=30, font=("Arial",14)); self.entrada_destino.pack(pady=5)

        # Información de tiempo aproximado
        self.etiqueta_tiempo_aproximado = self.crear_etiqueta("", 12, False)
        self.etiqueta_tiempo_aproximado.pack(anchor="w", pady=5)

        self.crear_boton("Limpiar selecciones", self.limpiar_selecciones, "#ff6666","white").pack(fill="x", pady=20)
        self.crear_boton("Calcular ruta", self.calcular_ruta, "#4CAF50","white").pack(fill="x", pady=10)
        self.interruptor_minusvalidos = self.crear_boton("Modo Accesibilidad: OFF", self.alternar_minusvalidos); self.interruptor_minusvalidos.pack(fill="x", pady=10)

        # Información de accesibilidad
        info_accesibilidad = tk.Label(self.marco_izquierdo, text="♿ Accesible  ⚠️ No accesible", 
                                    font=("Arial", 10), bg="#f0f0f0")
        info_accesibilidad.pack(pady=5)

        self.crear_etiqueta("Ruta Calculada:",14,True).pack(anchor="w", pady=(20,5))
        marco_ruta = tk.Frame(self.marco_izquierdo, bg="#f0f0f0"); marco_ruta.pack(fill="both", expand=True, pady=(0,10))
        barra_desplazamiento = tk.Scrollbar(marco_ruta); barra_desplazamiento.pack(side="right", fill="y")
        self.texto_ruta = tk.Text(marco_ruta,height=8,width=30,font=("Arial",11),wrap="word",yscrollcommand=barra_desplazamiento.set,bg="white",relief="solid",borderwidth=1,padx=5,pady=5)
        self.texto_ruta.pack(side="left", fill="both", expand=True); barra_desplazamiento.config(command=self.texto_ruta.yview)
        self.texto_ruta.config(state="disabled"); self.limpiar_texto_ruta()

    # --------------------- Mapa ---------------------
    def crear_mapa(self):
        self.marco_derecho = tk.Frame(self.raiz); self.marco_derecho.pack(side="right", fill="both", expand=True)
        plt.rcParams['toolbar']='None'; plt.switch_backend('TkAgg')
        self.fig,self.ejes = plt.subplots(figsize=(10,8),dpi=100)
        plt.subplots_adjust(left=0,bottom=0,right=1,top=1); self.ejes.set_aspect("equal"); self.ejes.axis("off")

        for linea, secuencia in self.secuencias_lineas.items():
            xs, ys = [], []
            for estacion in secuencia:
                x,y=self.coordenadas_linea[linea][estacion]; xs.append(x); ys.append(y)
                es_transbordo = sum(estacion in l for l in self.secuencias_lineas.values())>1
                es_accesible = self.controlador.es_estacion_accesible(estacion)
                color_interior = "lightgreen" if es_accesible else "white" if es_transbordo else "black"
                marcador = self.ejes.scatter(x,y,s=160 if es_transbordo else 80,facecolor=color_interior,
                                         edgecolor="black",linewidth=2 if es_transbordo else 1,zorder=3)
                self.marcadores_estaciones[estacion]=marcador
                dx,dy,alineacion_h,fuente=self.desplazamientos.get(estacion,(0.15,0.15,'left',10))
                self.ejes.text(x+dx,y+dy,estacion,fontsize=fuente,ha=alineacion_h,va="center",zorder=4)
            self.ejes.plot(xs,ys,color=self.COLORES[linea],linewidth=6,alpha=0.8,zorder=1)
        self.ejes.set_xlim(-8,11); self.ejes.set_ylim(-12,7)
        self.lienzo = FigureCanvasTkAgg(self.fig, master=self.marco_derecho); self.lienzo.get_tk_widget().pack(fill="both",expand=True)
        self.lienzo.draw()

    # --------------------- Utilidades ---------------------
    def color_estacion(self,nombre): 
        es_accesible = self.controlador.es_estacion_accesible(nombre)
        if es_accesible:
            return "lightgreen"
        else:
            return "white" if sum(nombre in l for l in self.secuencias_lineas.values())>1 else "black"
            
    def restaurar_colores(self):
        for nombre,marcador in self.marcadores_estaciones.items():
            if nombre==self.origen_seleccionado: 
                marcador.set_facecolor('green')
            elif nombre==self.destino_seleccionado: 
                marcador.set_facecolor('red')
            else: 
                marcador.set_facecolor(self.color_estacion(nombre))
        self.lienzo.draw()

    def limpiar_ruta(self):
        if self.linea_ruta: 
            self.linea_ruta.remove()
            self.linea_ruta = None
        self.restaurar_colores()
        
    def limpiar_texto_ruta(self):
        self.texto_ruta.config(state="normal")
        self.texto_ruta.delete(1.0,tk.END)
        self.texto_ruta.insert(1.0,"")
        self.texto_ruta.config(state="disabled")
        
    def limpiar_selecciones(self):
        self.origen_seleccionado = None
        self.destino_seleccionado = None
        self.entrada_origen.delete(0,tk.END)
        self.entrada_destino.delete(0,tk.END)
        self.etiqueta_tiempo_aproximado.config(text="")
        self.limpiar_ruta()
        self.limpiar_texto_ruta()

    def actualizar_tiempo_aproximado(self):
        """Actualiza la información de tiempo aproximado (solo en label, sin línea visual)"""
        if self.origen_seleccionado and self.destino_seleccionado:
            tiempo_aprox, distancia = self.controlador.calcular_tiempo_aproximado(
                self.origen_seleccionado, self.destino_seleccionado
            )
            
            texto = f"⏱️ Tiempo aprox: {tiempo_aprox:.1f} min | 📏 Distancia: {distancia/1000:.2f} km"
            self.etiqueta_tiempo_aproximado.config(text=texto)
        else:
            self.etiqueta_tiempo_aproximado.config(text="")

    # --------------------- Interacción ---------------------
    def al_hacer_clic(self, evento):
        if evento.inaxes != self.ejes: 
            return
            
        x_clic, y_clic = evento.xdata, evento.ydata
        estacion_cercana = None
        distancia_minima = float('inf')
        
        for nombre, (x, y) in self.coordenadas.items():
            distancia = (x - x_clic)**2 + (y - y_clic)**2
            if distancia < distancia_minima: 
                distancia_minima = distancia
                estacion_cercana = nombre
                
        if distancia_minima > 0.5 or not estacion_cercana: 
            return

        self.restaurar_colores()
        
        # Lógica de selección
        if not self.origen_seleccionado:
            self.origen_seleccionado = estacion_cercana
            self.entrada_origen.delete(0, tk.END)
            self.entrada_origen.insert(0, estacion_cercana)
            self.marcadores_estaciones[estacion_cercana].set_facecolor('green')
        elif not self.destino_seleccionado:
            self.destino_seleccionado = estacion_cercana
            self.entrada_destino.delete(0, tk.END)
            self.entrada_destino.insert(0, estacion_cercana)
            self.marcadores_estaciones[estacion_cercana].set_facecolor('red')
        else:
            # Si ya hay ambos, permitir cambiar haciendo clic nuevamente
            self.origen_seleccionado = estacion_cercana
            self.destino_seleccionado = None
            self.entrada_origen.delete(0, tk.END)
            self.entrada_origen.insert(0, estacion_cercana)
            self.entrada_destino.delete(0, tk.END)
            self.marcadores_estaciones[estacion_cercana].set_facecolor('green')
            self.limpiar_ruta()
            self.limpiar_texto_ruta()
        
        self.actualizar_tiempo_aproximado()
        self.lienzo.draw()

    # --------------------- Controlador ---------------------
    def calcular_ruta(self):
        """Calcula la ruta solo cuando se presiona el botón"""
        if self.origen_seleccionado and self.destino_seleccionado:
            self.controlador.calcular_ruta(self.origen_seleccionado, self.destino_seleccionado)
        else:
            self.mostrar_error("Seleccione origen y destino")
            
    def alternar_minusvalidos(self):
        self.modo_minusvalidos = not self.modo_minusvalidos
        self.controlador.toggle_minusvalidos(self.modo_minusvalidos)
        self.interruptor_minusvalidos.config(
            text=f"Modo Accesibilidad: {'ON' if self.modo_minusvalidos else 'OFF'}",
            bg="#4CAF50" if self.modo_minusvalidos else "#f0f0f0",
            fg="white" if self.modo_minusvalidos else "black"
        )
        self.restaurar_colores()
                                       
    def mostrar_ruta(self, ruta, tiempo_total=0, num_transbordos=0, es_accesible=False):
        self.limpiar_ruta()
        if len(ruta) < 2: 
            return
            
        puntos_x = [self.coordenadas[estacion][0] for estacion in ruta if estacion in self.coordenadas]
        puntos_y = [self.coordenadas[estacion][1] for estacion in ruta if estacion in self.coordenadas]
        
        if len(puntos_x) < 2: 
            return
        
        # Color de la ruta según accesibilidad
        color_ruta = 'green' if es_accesible else 'blue'
        self.linea_ruta, = self.ejes.plot(
            puntos_x, puntos_y, color=color_ruta, linewidth=8, alpha=0.7, zorder=2,
            marker='o', markersize=10, markerfacecolor='yellow'
        )
        
        for estacion in ruta:
            if estacion in self.marcadores_estaciones and estacion != self.origen_seleccionado and estacion != self.destino_seleccionado:
                self.marcadores_estaciones[estacion].set_facecolor('orange')
                
        self.actualizar_texto_ruta(ruta, tiempo_total, num_transbordos, es_accesible)
        self.lienzo.draw()

    def actualizar_texto_ruta(self, ruta, tiempo_total=0, num_transbordos=0, es_accesible=False):
        self.texto_ruta.config(state="normal")
        self.texto_ruta.delete(1.0, tk.END)
        
        if not ruta: 
            return
            
        # Formatear tiempo
        tiempo_formateado = f"{tiempo_total:.1f} minutos"
        if tiempo_total > 60:
            horas = int(tiempo_total // 60)
            minutos = int(tiempo_total % 60)
            tiempo_formateado = f"{horas}h {minutos}min"
        
        texto = f"Ruta: {ruta[0]} → {ruta[-1]}\n"
        texto += f"Tiempo: {tiempo_formateado}\n"
        texto += f"Transbordos: {num_transbordos}\n"
        texto += f"Estaciones: {len(ruta)}\n"
        texto += f"Accesible: {'Sí' if es_accesible else 'No'}\n"
        texto += "─" * 30 + "\n"
        
        # Listar estaciones con indicadores
        for i, estacion in enumerate(ruta):
            linea = ""
            if i == 0:
                linea = " ORIGEN"
            elif i == len(ruta) - 1:
                linea = " DESTINO"
            elif sum(estacion in l for l in self.secuencias_lineas.values()) > 1:
                linea = " TRANSBORDO"
            
            # Agregar indicador de accesibilidad
            accesible = " ♿" if self.controlador.es_estacion_accesible(estacion) else " ⚠️"
            
            texto += f"{i+1}. {estacion}{linea}{accesible}\n"
        
        self.texto_ruta.insert(1.0, texto)
        self.texto_ruta.config(state="disabled")
        
    def mostrar_error(self, mensaje): 
        etiqueta_error = tk.Label(
            self.marco_izquierdo, text=mensaje, 
            font=("Arial", 10), bg="#ffcccc", fg="red", wraplength=280
        )
        etiqueta_error.pack(pady=5)
        self.raiz.after(3000, etiqueta_error.destroy)
        
    def ejecutar(self): 
        self.raiz.mainloop()