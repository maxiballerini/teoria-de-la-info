import sys
import numpy as np
from collections import Counter
from itertools import product

def leer_archivo(nombre_archivo):
    # Abrir el archivo en modo lectura
    with open(nombre_archivo, 'rb') as archivo:
        # Leer el contenido del archivo
        contenido = archivo.read()  
        # Agregar cada carácter del contenido a la lista
    return contenido


def obtener_caracteres_unicos(contenido):
    # Obtiene una lista de caracteres únicos en el contenido
    return list(set(contenido))

def calcular_probabilidades(contenido, caracteres_unicos):
    # Cuenta las ocurrencias de cada byte en el contenido
    conteo_total = len(contenido)
    contador = Counter(contenido)
    
    # Calcula la probabilidad de cada carácter único
    probabilidades = [contador[caracter] / conteo_total for caracter in caracteres_unicos]
    return probabilidades

def calcular_entropia(vec_probabilidades):
    suma = 0
    for i in range(len(vec_probabilidades)):
        suma += vec_probabilidades[i]*np.log2(1/vec_probabilidades[i])

    return suma

ruta_archivo = "tp4_samples/tp4_sample0_sent.bin"
contenido_binario = leer_archivo(ruta_archivo)
caracteres_unicos = obtener_caracteres_unicos(contenido_binario)
vector_probabilidades = calcular_probabilidades(contenido_binario, caracteres_unicos)
entropia = calcular_entropia(vector_probabilidades)
print(f"a)Entropía: {entropia:.6f} binits")