import sys
import numpy as np
import random
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

def generaVectorProbabilidades(palabras, cant_simbolos_unicos):
    vectorProbabilidades = []
    for palabra in palabras:
        vectorProbabilidades.append(round((1 / cant_simbolos_unicos) ** (len(palabra)), 6))
    return vectorProbabilidades

def crea_archivo(nombre_archivo, N, vector_palabras_cifradas, vector_prob):
    with open(nombre_archivo, 'w', encoding='utf-8', errors='ignore') as arch:
        for i in range(N):
            palabra = montecarlo(vector_prob, vector_palabras_cifradas)
            arch.write(palabra)

def montecarlo(probabilidades, palabras):
    # Generar un número aleatorio entre 0 y 1
    r = random.random()
    
    # Inicializar el acumulador de probabilidades
    acumulador = 0.0
    
    # Iterar sobre las probabilidades y las palabras
    for i, p in enumerate(probabilidades):
        acumulador += p
        if r < acumulador:
            return palabras[i]  # Retorna la palabra seleccionada

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
    vectorProbabilidades = generaVectorProbabilidades(palabras, len(caracteres_unicos))
    print("Las palabras sí pueden generar un código compacto, sus probabilidades serían: ")
    print(palabras)
    print(vectorProbabilidades)
else:
    print("No es código instantáneo")



