from obtener_datos_por_cuit import obtener_datos_por_cuit
import os
from datetime import datetime


def crear_informe_txt(cuit, primerComprobante, ultimoComprobante, periodo, valorTotal,puntoDeVenta,carpeta):

    #Dependiendo de donde esta la carpeta que se eligio para procesar, en esa misma carpeta, se genera el reporte
    nombreArchivo = carpeta + "/reporteDeVentas - " + periodo + ".txt"

    with open(nombreArchivo, "a", encoding="utf-8") as archivo_txt:
        datosJSON = obtener_datos_por_cuit(int(cuit))
        razonSocial = datosJSON.get("RAZON SOCIAL")
        userGomez = datosJSON.get("USER")

        if userGomez == "-":
            userGomez = "Sin usuario definido"
    
        valorTotal = round(valorTotal,2)

        #Puedo poner unicamente 9 lineas en el txt, para que me salgan hasta 6 por hojas
        archivo_txt.write("------------------------------\n")
        archivo_txt.write(f"USER: {userGomez}\n")
        archivo_txt.write(f"CUIT: {cuit}\n")
        archivo_txt.write(f"Razon Social: {razonSocial}\n")
        archivo_txt.write(f"Punto de Venta: {puntoDeVenta}\n")
        if primerComprobante == "No se encontraron Facturas C en los datos":
            archivo_txt.write(f"<<{primerComprobante}>>\n")
        else:
            archivo_txt.write(f"Comprobantes desde <{primerComprobante}> hasta <{ultimoComprobante}>\n") 
        archivo_txt.write(f"Periodo: {periodo}\n")
        archivo_txt.write(f"Total: {valorTotal}\n")
        archivo_txt.write("------------------------------\n")

def crear_informe_errorFecha(cuit, carpeta,mes, anio):

    #Dependiendo de donde esta la carpeta que se eligio para procesar, en esa misma carpeta, se genera el reporte
    nombreArchivo = carpeta + "/reporte_de_error.txt"
    

    with open(nombreArchivo, "a", encoding="utf-8") as archivo_txt:
        datosJSON = obtener_datos_por_cuit(int(cuit))
        razonSocial = datosJSON.get("RAZON SOCIAL")
        userGomez = datosJSON.get("USER")

        mes, anio  = str(mes),str(anio)

        fecha = "01"+ mes + anio
        fecha = datetime.strptime(fecha, "%d%m%Y")
        
        periodo = fecha.strftime("%B %Y")
        periodo = periodo.upper()

        if userGomez == "-":
            userGomez = "Sin usuario definido"

        #Puedo poner unicamente 9 lineas en el txt, para que me salgan hasta 6 por hojas
        archivo_txt.write("------------------------------\n")
        archivo_txt.write(f"SIN VENTAS EN {periodo}\n")
        archivo_txt.write(f"USER: {userGomez}\n")
        archivo_txt.write(f"CUIT: {cuit}\n")
        archivo_txt.write(f"Razon Social: {razonSocial}\n")
        archivo_txt.write("------------------------------\n")