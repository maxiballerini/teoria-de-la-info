import sys
import math
import random
import os

def almacena_palabras_y_crea_abecedario_unico(nombre_archivo):
    """
    Esta función toma un archivo de texto, almacena todas las palabras en un vector y 
    también crea un conjunto de caracteres únicos (un 'abecedario') a partir del contenido del archivo.

    Parámetros:
    nombre_archivo: El nombre del archivo de texto que se va a leer.

    Retorna:
        - vector_palabras (list): Una lista con todas las palabras del archivo, separadas por espacios.
        - vector_caracteres_unicos (list): Una lista ordenada de todos los caracteres únicos (sin espacios) 
          encontrados en el archivo.
    """

    with open(nombre_archivo, 'r', encoding='utf-8', errors='ignore') as archivo:
        contenido = archivo.read()
        vector_palabras = contenido.split()  # Separar palabras por espacios
        caracteres_unicos = set(contenido.replace(" ", ""))  # Remover espacios
        vector_caracteres_unicos = sorted(list(caracteres_unicos))  # Convertir el conjunto a lista y ordenar
        return vector_palabras, vector_caracteres_unicos
    

def inecuacion_KraftMcMillan(palabras, r):
    """
    Calcula el valor de la inecuación de Kraft-McMillan para un conjunto de palabras, 
    utilizado en teoría de la información para verificar si un código es un código prefijo.

    Parámetros:
    palabras (list): Una lista de cadenas de texto (palabras).
    r (int): La base del sistema utilizado, por ejemplo, 2 para un código binario.

    Retorna:
    float: El resultado de la suma de la inecuación de Kraft-McMillan. 
           Si el valor es ≤ 1, el código es un código prefijo.
    """

    sumatoria = 0
    for palabra in palabras:
        longitud = len(palabra)  # Obtener la longitud de la palabra
        sumatoria += r ** (-longitud)    # Sumar r elevado a -longitud
    return sumatoria 

def codigo_instantaneo(palabras):
    """
    Verifica si un conjunto de palabras (códigos) es un código instantáneo (o código prefijo). 
    Un código es instantáneo si ninguna palabra es prefijo de otra palabra en el conjunto.

    Parámetros:
    palabras (list): Una lista de cadenas de texto (palabras).

    Retorna:
    bool: 
        - `True` si el conjunto de palabras es un código instantáneo (ninguna palabra es prefijo de otra).
        - `False` si alguna palabra es prefijo de otra palabra.
    """

    palabras = sorted(palabras, key=len)  # Ordena por longitud para reducir el numero de comparaciones
    for i in range(len(palabras)):
        for j in range(i + 1, len(palabras)):
            if palabras[j].startswith(palabras[i]):  # Si una palabra es prefijo de otra
                return False
    return True

def genera_vector_probabilidades(palabras, r):
    """
    Genera un vector de probabilidades para un conjunto de palabras basado en su longitud, 
    usando la fórmula (1 / r) ^ longitud(palabra).

    Parámetros:
    palabras (list): Una lista de cadenas de texto (palabras).
    r (int): La base del sistema.

    Retorna:
    list: Una lista de probabilidades para cada palabra.
    """

    vectorProbabilidades = []
    for palabra in palabras:
        vectorProbabilidades.append(round((1 / r) ** (len(palabra)), 6))
    return vectorProbabilidades

def calcula_entropia(vector_probabilidades, base):
    """
    Calcula la entropía de un conjunto de probabilidades utilizando la fórmula de Shannon,
    que mide la cantidad de información promedio contenida en un conjunto de eventos.

    Parámetros:
    vector_probabilidades (list): Una lista de probabilidades (valores entre 0 y 1).
    base (int): La base del logaritmo utilizado para el cálculo de la entropía.

    Retorna:
    float: El valor de la entropía.
    """

    entropia = 0
    for valor in vector_probabilidades:
        entropia += valor * math.log(1/valor, base)
    return round(entropia, 3)

def calcula_longitud_media(palabras, vector_probabilidades):
    """
    Calcula la longitud media ponderada de un conjunto de palabras, 
    considerando sus probabilidades asociadas.

    Parámetros:
    palabras (list): Una lista de cadenas de texto (palabras).
    vector_probabilidades (list): Una lista de probabilidades asociadas a cada palabra.

    Retorna:
    float: La longitud media ponderada de las palabras.
    """

    longitud_media = 0
    for i in range(len(palabras)):
        longitud_media += len(palabras[i]) * vector_probabilidades[i]
    return round(longitud_media, 3)

def crea_archivo(nombre_archivo, N, vector_palabras_cifradas, vector_prob):
    """
    Crea un archivo de texto y escribe en él palabras seleccionadas a partir de un vector de probabilidades,
    utilizando el método de Monte Carlo.

    Parámetros:
    nombre_archivo (str): El nombre del archivo que se creará.
    N (int): La cantidad de palabras que se escribirán en el archivo.
    vector_palabras_cifradas (list): Una lista de palabras cifradas entre las cuales se seleccionarán las palabras a escribir.
    vector_prob (list): Una lista de probabilidades asociadas a las palabras cifradas.
    """

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