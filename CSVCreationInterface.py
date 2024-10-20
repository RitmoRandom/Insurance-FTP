import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class FTPHandlerB(FileSystemEventHandler):
    def on_modified(self, event):
        
        # Detectar si es un archivo CSV
        if not event.is_directory and event.src_path.endswith(".csv"):
            print(f"Detectado respuesta: {event.src_path}")
            self.modificar_csv(event.src_path)
            
    def modificar_csv(self, archivo):
        try:
            # Leer el archivo CSV
            df = pd.read_csv(archivo)
            #cuadro_texto.insert(tk.END, "¡Hola, mundo!\n")
            print(f"Respuesta:")
            print(df)
        except Exception as e:
            print(f"Error al modificar el archivo CSV: {e}")

def generar_csv():
    datos = {
        'Numero de Poliza': ['12345', '67890', '54321'],
        'Monto del Reclamo': [1000, 2500, 3500],
        'Fecha de Siniestro': ['2023-10-01', '2023-10-02', '2023-10-03'],
        'Descripcion del Siniestro': ['Accidente automovilistico', 'Incendio', 'Afectacion por tormenta']
    }
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    carpeta_salida = os.path.join(ruta_actual, "FTP")
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    df = pd.DataFrame(datos)
    nombre_archivo = "reclamos_seguros.csv"
    ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)
    try:
        df.to_csv(ruta_archivo, index=False)
        monitorizar_carpeta_ftp()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")
        
        
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

ventana = tk.Tk()
ventana.title("Generador de Archivos CSV - Seguros Globales")
ventana.geometry("400x200")
label = tk.Label(ventana, text="Generar archivo de reclamos de seguros en formato CSV")
label.pack(pady=20)
boton = tk.Button(ventana, text="Generar CSV", command=generar_csv)
boton.pack(pady=20)
cuadro_texto = tk.Text(ventana, height=10, width=30)
cuadro_texto.pack(pady=10)
ventana.mainloop()
