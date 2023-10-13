import json
import os
import tkinter as tk
from tkinter import simpledialog, filedialog
from tkinter import messagebox
import pandas as pd
import time
from datetime import datetime
import locale
#from crearPDF import crearPDF

from crear_informe_txt import crear_informe_txt, crear_informe_errorFecha
from creadorDeData import crearPDF

# Variables globales para rastrear el estado del procesamiento
archivos_procesados = 0
archivos_generados = 0
errores = False
tiempo_inicio = 0

# FUNCION PARA VER CUANTOS ARCHIVOS JSON HAY QUE PROCESAR

def procesar_carpeta(carpeta,procesoElegido,periodo):

    global archivos_procesados, archivos_generados, errores,tiempo_inicio
    archivos_procesados = 0
    archivos_generados = 0
    errores = False
    tiempo_inicio = time.time()

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".json"):
            ruta_archivo = os.path.join(carpeta, archivo)
            archivos_procesados += 1
            try:
                cargar_json(ruta_archivo,carpeta,procesoElegido,periodo)
                archivos_generados += 1
            except Exception as e:
                print(f"Error al procesar {ruta_archivo}: {e}")
                errores = True

    mostrar_resumen()

# FUNCION PARA CARGAR EL JSON Y MOSTRAR POR CONSOLA LOS VALORES DESEADOS DEL JSON


def cargar_json(ruta,carpeta,procesoElegido,periodo):
    diaInicio = "01"
    diaFin = periodo[:2]
    mes = periodo[2:4]
    anio = periodo[4:]

    diaInicio = int(diaInicio)
    diaFin = int(diaFin)
    mes = int(mes)
    anio = int(anio)

    try:
        with open(ruta, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        data_cuit = json_data.get("CUIT")
        data_dict = json_data.get("datosFacturacion", [])
        # Establecer la configuración regional a español
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

        # Inicializar variables
       
        primerComprobante = None  # Inicialmente no se conoce
        ultimoComprobante = None  # Inicialmente no se conoce
        periodo = None  # Inicialmente no se conoce
        puntoDeVenta = None
        #Aca tengo que definir lso acumuladores, de ventas y de notas de credito
        totalPositivo = 0
        totalNegativo = 0
        #Tengo que crear un arreglo para ir guardando los datos de los comprobantes para luego mandarlo a crearPDF
        
        
        datosComprobante = []

        for i, item in enumerate(data_dict):
            if "Fecha" in item:
                fecha = datetime.strptime(item["Fecha"], "%d/%m/%Y")
                periodo = fecha.strftime("%B %Y")
        
                # Definir el rango de fechas deseado (por ejemplo, agosto de 2023)
                fecha_inicio = datetime(anio, mes, diaInicio)
                fecha_fin = datetime(anio, mes, diaFin)
        
                if fecha_inicio <= fecha <= fecha_fin:
                    # Continuar con el procesamiento solo si la fecha está dentro del rango
                    datos_comprobante_actual = {}
                    for clave in ["Fecha", "Tipo", "Punto de Venta", "Número Desde", "Nro. Doc. Receptor", "Denominación Receptor", "Imp. Total"]:
                        if clave in item:
                            if clave == "Tipo":
                                if item[clave] == "13 - Nota de Crédito C":
                                    totalNegativo += item.get("Imp. Total", 0)
                                elif item[clave] == "9 - Recibo C":
                                    totalPositivo = totalPositivo    
                                elif item[clave] == "213 - Nota de Crédito Electrónica MiPyMEs (FCE) C":
                                    totalNegativo += item.get("Imp. Total", 0)
                                else: 
                                    totalPositivo += item.get("Imp. Total", 0)
                            datos_comprobante_actual[clave] = item[clave]
            
                    datosComprobante.append(datos_comprobante_actual)
            
                    if item["Tipo"] == "11 - Factura C":
                        if primerComprobante is None:
                            primerComprobante = item.get("Número Desde")
                        ultimoComprobante = item.get("Número Desde")
            else:
                print(f"Archivo: {ruta}")
        if primerComprobante is None:
            primerComprobante = "No se encontraron Facturas C en los datos"
        # Añadir manejo de excepción si no se encontraron datos en el rango de fechas
        if not datosComprobante:
            raise Exception("No se encontraron datos en el rango de fechas deseado.")

        #print("----")
        puntoDeVenta = (datosComprobante[0].get("Punto de Venta"))
        valorTotal = totalPositivo - totalNegativo
        #crearPDF(data_cuit, primerComprobante, ultimoComprobante, periodo, valorTotal,datosComprobante)
        #createPDF(data_cuit,puntoDeVenta,periodo,valorTotal,datosComprobante,carpeta)
        if procesoElegido == "Informe TXT":
            crear_informe_txt(data_cuit,primerComprobante,ultimoComprobante,periodo,valorTotal,puntoDeVenta,carpeta)
        else:
            #Aca voy a crear para llamar a Crear pdf
            crearPDF(data_cuit, puntoDeVenta, periodo, valorTotal, datosComprobante, carpeta)
            #print("Otro proceso")
        #print("----")

    except Exception as e:
        if str(e) == "No se encontraron datos en el rango de fechas deseado.":
            print("Error: ",e)
            crear_informe_errorFecha(data_cuit,carpeta,mes,anio)


#Funcion para leer los datos que tengo cargado en un JSON, para poder tener Razon Social, y otros datos

#Funcion para mostrar un resumen del proceso completo, mostrando tiempo y archivos
def mostrar_resumen():
    global archivos_procesados, archivos_generados, errores, tiempo_inicio
    tiempo_fin = time.time()
    tiempo_transcurrido = tiempo_fin - tiempo_inicio
    tiempo_transcurrido_formateado = time.strftime("%H:%M:%S", time.gmtime(tiempo_transcurrido))

    mensaje = f"Archivos procesados: {archivos_procesados}\nArchivos generados: {archivos_generados}\n"
    mensaje += f"Tiempo empleado: {tiempo_transcurrido_formateado}\n"
    if errores:
        mensaje += "\nHubo errores durante el procesamiento."

    messagebox.showinfo("Resumen del Proceso", mensaje)

# Función para seleccionar la carpeta a analizar para procesar los archivos
def seleccionar_carpeta(procesoElegido):
    # Pedir al usuario que ingrese el período
    periodo = simpledialog.askstring("Ingresar Periodo", "Por favor, ingresa el período (Formato ddmmaaaa):")
    if periodo is not None:
        carpeta = filedialog.askdirectory()
        if carpeta:
            procesar_carpeta(carpeta, procesoElegido, periodo)

# Crear la ventana de la aplicación
ventana = tk.Tk()
ventana.title("Seleccionar Carpeta con Archivos JSON")

ventana.geometry("400x300")
instrucciones = tk.Label(ventana, text="Script para procesar archivos JSON en una carpeta")
lugarBBDD = tk.Label(ventana, text="Base de Datos de Clientes >>> C:/data/bbdd.json")
instrucciones.pack(pady=10)
lugarBBDD.pack(pady=10)

# Botón para seleccionar la carpeta y el proceso elegido
boton_txt = tk.Button(ventana, text="Seleccionar Carpeta - Informe TXT", command=lambda: seleccionar_carpeta("Informe TXT"))
boton_pdf = tk.Button(ventana, text="Seleccionar Carpeta - Informe PDF", command=lambda: seleccionar_carpeta("Informe PDF"))
boton_txt.pack(pady=20)
boton_pdf.pack(pady=20)
boton_cancelar = tk.Button(ventana, text="Cancelar", command=ventana.quit)
boton_cancelar.pack(pady=10)

ventana.mainloop()