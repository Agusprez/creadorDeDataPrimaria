from obtener_datos_por_cuit import obtener_datos_por_cuit
from procesoPDF import texto_a_pdf, texto_a_pdf_PAGINADO
from prettytable import PrettyTable
from reportlab.lib.pagesizes import  A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import locale

dir_actual = os.path.dirname(__file__)

def crearPDF(cuit, punto_de_venta, periodo, valor_total, datos_comprobante, carpeta):
  datosJSON = obtener_datos_por_cuit(int(cuit))

  #Archivo a crear 
  nombreArchivoTXT = carpeta +"/" + datosJSON.get("RAZON SOCIAL") + " - " +periodo +".txt"
  nombreArchivoPDF = carpeta +"/" + datosJSON.get("RAZON SOCIAL") + " - " +periodo +".pdf"

  #OJO CON LEGAJO

  USER = datosJSON.get("USER")
  CONTRIBUYENTE = datosJSON.get("RAZON SOCIAL")
  LEGAJO = datosJSON.get("LEGAJO")
  periodo = periodo.upper() 
  #Consideraciones para datos sin valor

  if LEGAJO == "-" or LEGAJO == None:
    LEGAJO = "SIN LEGAJO"

  if USER == "-":
    USER = "SIN USUARIO DEFINIDO"

  
  #print(f"USER: {USER}")
  #print(f"CUIT: {cuit}")
  #print(f"CONTRIBUYENTE: {CONTRIBUYENTE}")
  #print(f"LEGAJO: {LEGAJO}")
  #print(f"PUNTO DE VENTA: {punto_de_venta}")
  #print(f"PERIODO: {periodo}")
  #print(f"TOTAL: {valor_total}")

  #para el "encabezado", voy a imprimir USER, CUIT, CONTRIBUYENTE, LEGAJO, PUNTO DE VENTA Y PERIODO (LO TRAIGO POR PARAMETRO)
  
  #Tengo que lograr que el ancho total no supere NUNCA los 80 caracteres
  tablaDeComprobantes = PrettyTable() 
  tablaDeComprobantes.field_names = ["Fecha", "Tipo", "Nro", "CUIT", "Razon Social", "Total"]
  #tablaDeComprobantes.align["Nro"] = "r"
  tablaDeComprobantes.align["Total"] = "r"
  # 10 - 10 - 8 - 11 - 16 - 10
  tablaDeComprobantes.add_row(["          ","    ","        ","           ","                    ","              "])
  
  for elemento in datos_comprobante:
    
    tipoDeComp = nombreComp(elemento)
    valorComp = formatear_numero(elemento["Imp. Total"])


    if elemento["Nro. Doc. Receptor"] == 0.0:
      nroDocReceptor = ""
    else: 
      nroDocReceptor = elemento["Nro. Doc. Receptor"]

    if elemento["Denominación Receptor"] == 0.0:
      denomReceptor = "CONS. FINAL"
    else: 
      denomReceptor = elemento["Denominación Receptor"][:20]
    
    
      

    tablaDeComprobantes.add_row([elemento["Fecha"], tipoDeComp, elemento["Número Desde"], 
                                 nroDocReceptor, 
                                 denomReceptor, 
                                 valorComp])

  valor_total = formatear_numero(valor_total)
  tablaDeComprobantes.add_row(["","","","","",""])
  tablaDeComprobantes.add_row(["","","","","Importe Total",valor_total])


  # Abre el archivo en modo escritura
  with open(nombreArchivoTXT, "w") as archivo:

    # Escribe los datos en el archivo
    archivo.write(f"USER: {USER}\n")
    archivo.write(f"CUIT: {cuit}\n")
    archivo.write(f"CONTRIBUYENTE: {CONTRIBUYENTE}\n")
    archivo.write(f"LEGAJO: {LEGAJO}\n")
    archivo.write(f"PUNTO DE VENTA: {punto_de_venta}\n")
    archivo.write(f"PERIODO: {periodo}\n")

    # Escribe la tabla en el archivo
    archivo.write(str(tablaDeComprobantes))

    #print(f"Los datos se han guardado en el archivo: {nombreArchivoTXT}")
    #procesamientoPDF(nombreArchivoTXT, nombreArchivoPDF)
  try:
     with open(nombreArchivoTXT, 'r') as archivo:
        lineas = archivo.readlines()
        cantidadLineas = len(lineas)
        if cantidadLineas < 55:
          texto_a_pdf(nombreArchivoTXT, nombreArchivoPDF)
        else:
          texto_a_pdf_PAGINADO(nombreArchivoTXT, nombreArchivoPDF)
          #print(f"Supera limite de lineas a procesar {nombreArchivoTXT}")     

  except FileNotFoundError:
    print("El archivo no se encuentra en la ruta especificada.")
  except Exception as e:
    print("Ocurrió un error al intentar leer el archivo:", str(e))



  #print (tablaDeComprobantes)

def nombreComp(elemento):
    if "Tipo" in elemento:
        tipoDeComp = elemento["Tipo"]
        if tipoDeComp == "11 - Factura C": 
          tipoDeComp = "FC"
        elif tipoDeComp == "13 - Nota de Crédito C":
          tipoDeComp = "NC"
    return tipoDeComp

def formatear_numero(numero):
    # Establecer la configuración local para el formateo
    locale.setlocale(locale.LC_ALL, '')  # Utiliza la configuración regional predeterminada del sistema

    # Convertir el número a punto flotante
    numero_flotante = float(numero)

    # Aplicar el formato con separadores de miles y dos decimales
    numero_formateado = locale.format("%.2f", numero_flotante, grouping=True)
    
    return numero_formateado