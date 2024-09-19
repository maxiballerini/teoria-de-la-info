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
    
nombre_archivo = "C:/teoria-de-la-info/TP-2/tp2_sample0.txt"
palabras, caracteres_unicos = almacenar_palabras_y_crear_abecedario_unico(nombre_archivo)
print(palabras)
print(caracteres_unicos)