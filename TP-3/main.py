import os
from collections import Counter

def abrir_archivo(nombre_archivo):
    # Abriendo un archivo de imagen en modo binario
    with open(nombre_archivo, "rb") as archivo:
        contenido_binario = archivo.read()  # Lee todo el contenido del archivo como bytes

    #print(contenido_binario)  # Imprime los bytes, puedes procesarlos o guardarlos en un arreglo

    #Contar la frecuencia de cada byte
    conteo_bytes = Counter(contenido_binario)

    #Separar los bytes únicos y sus frecuencias en dos listas
    bytes_unicos = list(conteo_bytes.keys())
    frecuencia_bytes = list(conteo_bytes.values())

    #print("Bytes únicos:", bytes_unicos)
    #print("Frecuencia de bytes:", frecuencia_bytes)
    return contenido_binario

def obtener_probabilidades(contenido):
    #Función que obtiene las probabilidades de cada símbolo(byte), devuelve un diccionario (byte-probabilidad)

    total = len(contenido)
    conteo_bytes = Counter(contenido) # Contador que tiene cada byte y cuantas veces aparece
    res = {}
    for byte_unico, frec in conteo_bytes.items():
        res[byte_unico] = float(frec) / total
    #res = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
    return res

# Obtener el directorio donde se encuentra el script
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Combinar la ruta de la carpeta con el nombre del archivo
#ruta_completa = os.path.join(directorio_actual, "prueba.txt")
ruta_completa = os.path.join(directorio_actual, "facultad.png")
# Leemos el archivo de entrada y lo almacenamos
contenido_binario = abrir_archivo(ruta_completa)
# Calculamos la distribución de probabilidades para cada símbolo
probabilidades = obtener_probabilidades(contenido_binario)

print(probabilidades)