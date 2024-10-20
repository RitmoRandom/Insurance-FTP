import time
import os
import pandas as pd
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
def transformar_valor(valor):
        if valor == 1:
            return 'aprobado'
        elif valor == 2:
            return 'rechazado'
        elif valor == 3:
            return 'falta de datos'
class FTPHandlerB(FileSystemEventHandler):
    def on_created(self, event):
        # Detectar si es un archivo CSV
        if not event.is_directory and event.src_path.endswith(".csv"):
            print(f"Nuevo archivo detectado: {event.src_path}")
            self.modificar_csv(event.src_path)
    
    def modificar_csv(self, archivo):
        try:
            # Leer el archivo CSV
            df = pd.read_csv(archivo)
            valores_aleatorios = np.random.randint(1, 4, size=len(df))
            df['Aprobacion'] = [transformar_valor(valor) for valor in valores_aleatorios]
            
            # Guardar el archivo CSV modificado en la carpeta FTP
            df.to_csv(archivo, index=False)
            print(f"Archivo CSV procesado")
        except Exception as e:
            print(f"Error al modificar el archivo CSV: {e}")
            


def monitorizar_carpeta_ftp():
    carpeta_ftp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FTP")
    
    event_handler = FTPHandlerB()
    observer = Observer()
    observer.schedule(event_handler, carpeta_ftp, recursive=False)
    
    observer.start()
    print(f"Monitorizando la carpeta: {carpeta_ftp}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    # Iniciar monitorización de la carpeta FTP
    monitorizar_carpeta_ftp()