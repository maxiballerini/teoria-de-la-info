import sys
import numpy as np
from collections import Counter
from itertools import product

def almacenar_palabras_y_crear_abecedario_unico(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8', errors='ignore') as archivo:
        contenido = archivo.read()
        vector_palabras = contenido.split()  # Separar palabras por espacios
        caracteres_unicos = set(contenido.replace(" ", ""))  # Remover espacios
        vector_caracteres_unicos = sorted(list(caracteres_unicos))  # Convertir el conjunto a lista y ordenar
        return vector_palabras, vector_caracteres_unicos
    

def inecuacionKraftMcMillan(r, palabras):
    sumatoria = 0
    for palabra in palabras:
        longitud = len(palabra)  # Obtener la longitud de la palabra
        sumatoria += r ** -longitud    # Sumar r elevado a -longitud
    return sumatoria <= 1 

def codigoInstantaneo(palabras):
    palabras = sorted(palabras, key=len)  # Ordena por longitud para reducir el numero de comparaciones
    for i in range(len(palabras)):
        for j in range(i + 1, len(palabras)):
            if palabras[j].startswith(palabras[i]):  # Si una palabra es prefijo de otra
                return False
    return True


nombre_archivo = "tp2_sample0.txt"
palabras, caracteres_unicos = almacenar_palabras_y_crear_abecedario_unico(nombre_archivo)
print(palabras)
print(caracteres_unicos)

if inecuacionKraftMcMillan(len(caracteres_unicos), palabras):
    print("Cumple la inecuación de Kraft-McMillan")
else:
    print("No cumple la inecuación de Kraft-McMillan")

if codigoInstantaneo(palabras):
    print("Es código instantáneo")
else:
    print("No es código instantáneo")



