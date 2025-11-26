import sys
import os

# Añadir las carpetas al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'CONTROLADOR'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'VISTA'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'MODELO'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'DATA'))

from CONTROLADOR.controlador_metro import ControladorMetro
from VISTA.fomo import InterfazMetro

def main():
    print("Iniciando Sistema Metro CDMX...")
    
    # Crear controlador
    controlador = ControladorMetro()
    
    # Crear vista con el controlador
    vista = InterfazMetro(controlador)
    
    # Ejecutar aplicación
    vista.ejecutar()

if __name__ == "__main__":
    main()