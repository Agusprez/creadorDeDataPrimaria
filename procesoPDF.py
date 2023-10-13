from reportlab.lib.pagesizes import  A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

dir_actual = os.path.dirname(__file__)


def texto_a_pdf(archivo_txt, archivo_pdf):
   #Deberia generar una condicion que cuando el archivo tenga menos de 54 lineas, haga el proceso normal
   
    # Abre el archivo de texto para lectura
    with open(archivo_txt, 'r') as archivo:
       lineas = archivo.readlines()  
       
    # Carga la fuente "Courier New" (asegúrate de tener la fuente instalada en tu sistema)
    fuente = os.path.join(dir_actual, "Courier_New.ttf")
    pdfmetrics.registerFont(TTFont('CourierNew', fuente))
    #pdfmetrics.registerFont(TTFont('CourierNew', 'Courier_New.ttf'))

    # Crea un archivo PDF con el tamaño de página A4 en orientación horizontal
    c = canvas.Canvas(archivo_pdf, pagesize=(A4))

    
    # Configura la fuente "Courier New" y el tamaño de fuente
    c.setFont('Courier-Bold', 12)

    # Calcula el ancho y alto de la página A4 en orientación horizontal
    ancho, alto = (A4)

# Divide las líneas en grupos de 63
    grupos_lineas = [lineas[i:i+54] for i in range(0, len(lineas), 54)]

    for grupo in grupos_lineas:
        # Inicializa la posición de escritura en la página
        x, y = 50, alto - 50
        # Configura la fuente y el tamaño de fuente
        c.setFont('Courier-Bold', 10)

        # Agrega cada línea al PDF
        for linea in grupo:
            c.drawString(x, y, linea.rstrip('\n'))  # strip() elimina saltos de línea adicionales
            y -= 14  # Espacio entre líneas

        # Agrega un salto de página al final de cada grupo
        c.drawString(ancho - 100, alto - 30, f"Página 1")

        c.showPage()

    # Cierra el archivo PDF
    c.save()

def texto_a_pdf_PAGINADO(archivo_txt, archivo_pdf):
   
    # Abre el archivo de texto para lectura
    with open(archivo_txt, 'r') as archivo:
      lineas = archivo.readlines()  
      encabezado = lineas[:9]
      restoDatos = lineas[10:]

    # Carga la fuente "Courier New" (asegúrate de tener la fuente instalada en tu sistema)
    fuente = os.path.join(dir_actual, "Courier_New.ttf")
    pdfmetrics.registerFont(TTFont('CourierNew', fuente))
    #pdfmetrics.registerFont(TTFont('CourierNew', 'Courier_New.ttf'))

    # Crea un archivo PDF con el tamaño de página A4 en orientación horizontal
    c = canvas.Canvas(archivo_pdf, pagesize=(A4))

    
    # Configura la fuente "Courier New" y el tamaño de fuente
    c.setFont('Courier-Bold', 12)

    # Calcula el ancho y alto de la página A4 en orientación horizontal
    ancho, alto = (A4)
    lineas_por_pagina = 44
    grupos_lineas = [restoDatos[i:i+lineas_por_pagina] for i in range(0, len(restoDatos), lineas_por_pagina)]

    for numero_pagina, grupo in enumerate(grupos_lineas, start=1):
        # Inicializa la posición de escritura en la página
        x, y = 50, alto - 50

        # Agrega el encabezado al inicio de cada página
        for linea_encabezado in encabezado:
            c.setFont('Courier-Bold', 10)
            c.drawString(x, y, linea_encabezado.rstrip('\n'))
            y -= 14

        # Configura la fuente y el tamaño de fuente
        c.setFont('Courier-Bold', 10)

        # Agrega cada línea al PDF
        for linea in grupo:
            c.drawString(x, y, linea.rstrip('\n'))  # strip() elimina saltos de línea adicionales
            y -= 14  # Espacio entre líneas

        # Agrega el número de página en la esquina superior derecha de la página
        c.drawString(ancho - 100, alto - 30, f"Página {numero_pagina}")

        # Agrega un salto de página al final de cada grupo
        c.showPage()

    # Cierra el archivo PDF
    c.save()