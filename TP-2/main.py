import sys
import math
import random
import os

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
    longitud_media = 0
    for i in range(len(palabras)):
        longitud_media += len(palabras[i]) * vector_probabilidades[i]
    return round(longitud_media, 3)

def crea_archivo(nombre_archivo, N, vector_palabras_cifradas, vector_prob):
    # Obtener el directorio donde se encuentra el script
    directorio_actual = os.path.dirname(os.path.abspath(__file__))

    # Combinar la ruta de la carpeta con el nombre del archivo
    ruta_completa = os.path.join(directorio_actual, nombre_archivo)

    with open(ruta_completa, 'w', encoding='utf-8', errors='ignore') as arch:
        for i in range(N):
            palabra = montecarlo(vector_prob, vector_palabras_cifradas)
            arch.write(palabra)
        print("\ne) Archivo de salida generado exitosamente")


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

if len(sys.argv) > 1:
    nombre_archivo = sys.argv[1]
    palabras, caracteres_unicos = almacena_palabras_y_crea_abecedario_unico(nombre_archivo)
    print(f"\na) Conjunto de palabras: {palabras}")
    print(f"\nCaracteres únicos: {caracteres_unicos}")

    suma_kraft = inecuacion_KraftMcMillan(palabras, len(caracteres_unicos))
    # print(f"K =  {suma_kraft}")

    if suma_kraft <= 1:
        print("\nb) Cumple la inecuación de Kraft-McMillan")

        if codigo_instantaneo(palabras):
            print("\nEs código instantáneo")

        else:
            print("\nNo es código instantáneo")

        if suma_kraft == 1:
            vector_probabilidades = genera_vector_probabilidades(palabras, len(caracteres_unicos))
            print("\nc) Las palabras sí podrían generar un código compacto, sus probabilidades deberían ser: ")
            print(vector_probabilidades)

            entropia = calcula_entropia(vector_probabilidades, len(caracteres_unicos))
            print(f"\nd) Entropía de la fuente: {entropia}")

            longitud_media = calcula_longitud_media(palabras, vector_probabilidades)
            print(f"\nLongitud media del código: {longitud_media}")
            if len(sys.argv) > 3:
                N = int(sys.argv[3])
                crea_archivo("output.txt", N, palabras, vector_probabilidades)
        else:
            print("\nc) No es posible que las palabras formen un código compacto")
            if len(sys.argv) > 3:
                print("\ne) No es posible generar el archivo")
    else:
        print("\nb) No cumple la inecuación de Kraft-McMillan")
        print("\nc) No es posible que las palabras formen un código compacto")
        if len(sys.argv) > 3:
            print("\ne) No es posible generar el archivo")