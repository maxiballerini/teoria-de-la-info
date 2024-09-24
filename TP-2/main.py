import sys
import numpy as np
import math
import random
from collections import Counter
from itertools import product

def almacena_palabras_y_crea_abecedario_unico(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8', errors='ignore') as archivo:
        contenido = archivo.read()
        vector_palabras = contenido.split()  # Separar palabras por espacios
        caracteres_unicos = set(contenido.replace(" ", ""))  # Remover espacios
        vector_caracteres_unicos = sorted(list(caracteres_unicos))  # Convertir el conjunto a lista y ordenar
        return vector_palabras, vector_caracteres_unicos
    

def inecuacion_KraftMcMillan(palabras, r):
    sumatoria = 0
    for palabra in palabras:
        longitud = len(palabra)  # Obtener la longitud de la palabra
        sumatoria += r ** (-longitud)    # Sumar r elevado a -longitud
    return sumatoria 

def codigo_instantaneo(palabras):
    palabras = sorted(palabras, key=len)  # Ordena por longitud para reducir el numero de comparaciones
    for i in range(len(palabras)):
        for j in range(i + 1, len(palabras)):
            if palabras[j].startswith(palabras[i]):  # Si una palabra es prefijo de otra
                return False
    return True

def genera_vector_probabilidades(palabras, r):
    vectorProbabilidades = []
    for palabra in palabras:
        vectorProbabilidades.append(round((1 / r) ** (len(palabra)), 6))
    return vectorProbabilidades

def calcula_entropia(vector_probabilidades, base):
    entropia = 0
    for valor in vector_probabilidades:
        entropia += valor * math.log(1/valor, base)
    return round(entropia, 3)

def calcula_longitud_media(palabras, vector_probabilidades):
    longitudMedia = 0
    for i in range(len(palabras)):
        longitudMedia += len(palabras[i]) * vector_probabilidades[i]
    return round(longitudMedia, 3)

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

nombre_archivo = "tp2_sample7.txt"
palabras, caracteres_unicos = almacena_palabras_y_crea_abecedario_unico(nombre_archivo)
print(palabras)
print(caracteres_unicos)

suma_kraft = inecuacion_KraftMcMillan(palabras, len(caracteres_unicos))
print(f"K =  {suma_kraft}")

if suma_kraft <= 1:
    print("Cumple la inecuación de Kraft-McMillan")

    if codigo_instantaneo(palabras):
        print("Es código instantáneo")

    else:
        print("No es código instantáneo")

    if suma_kraft == 1:
        vector_probabilidades = genera_vector_probabilidades(palabras, len(caracteres_unicos))
        print("Las palabras sí podrían generar un código compacto, sus probabilidades deberían ser: ")
        print(palabras)
        print(vector_probabilidades)

        entropia = calcula_entropia(vector_probabilidades, len(caracteres_unicos))
        print(f"Entropía de la fuente: {entropia}")

        longitud_media = calcula_longitud_media(palabras, vector_probabilidades)
        print(f"Longitud media del código: {longitud_media}")
    else:
        print("No es posible que las palabras formen un código compacto")
else:
    print("No cumple la inecuación de Kraft-McMillan")




