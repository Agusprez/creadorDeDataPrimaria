import json

#Debe recibir por parametro el tipo de dato INT
def obtener_datos_por_cuit(cuit):
    try:
        with open('C:/data/bbdd.json', 'r') as archivo:
            datos = json.load(archivo)
            for entrada in datos:
                if entrada.get("CUIT") == cuit:
                    return entrada
            return {"error": "CUIT no encontrado"}
    except FileNotFoundError:
        return {"error": "Archivo JSON no encontrado"}
    except Exception as e:
        return {"error": str(e)}
