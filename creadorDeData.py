from obtener_datos_por_cuit import obtener_datos_por_cuit

def crearPDF(cuit, punto_de_venta, periodo, valor_total, datos_comprobante, carpeta):
  datosJSON = obtener_datos_por_cuit(int(cuit))

  #Archivo a crear 
  nombreArchivoTXT = carpeta +"/" + datosJSON.get("RAZON SOCIAL") + " - " +periodo +".txt"

  #OJO CON LEGAJO

  USER = datosJSON.get("USER")
  CONTRIBUYENTE = datosJSON.get("RAZON SOCIAL")
  LEGAJO = datosJSON.get("LEGAJO ")

  #Consideraciones para datos sin valor

  if LEGAJO == "-":
    LEGAJO = "SIN LEGAJO"

  if USER == "-":
    USER = "SIN USUARIO DEFINIDO"

  print(f"USER: {USER}")
  print(cuit)
  print(CONTRIBUYENTE)
  print(LEGAJO)
  print(punto_de_venta)
  print(periodo)
  print(valor_total)

  #para el "encabezado", voy a imprimir USER, CUIT, CONTRIBUYENTE, LEGAJO, PUNTO DE VENTA Y PERIODO (LO TRAIGO POR PARAMETRO)
  
  