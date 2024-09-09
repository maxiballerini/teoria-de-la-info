import sys
import numpy as np
from collections import Counter
from itertools import product

def leer_archivo(nombre_archivo):
    """
    Lee un archivo y guarda su contenido en una lista

    Parámetros:
    nombre_archivo (str): El nombre del archivo
    
    Retorna:
    list: Los caracteres del archivo en una lista
    """

    # Inicializar una lista para almacenar los caracteres
    vector_caracteres = []
    # Abrir el archivo en modo lectura
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        # Leer el contenido del archivo
        contenido = archivo.read()  
        # Agregar cada carácter del contenido a la lista
        vector_caracteres.extend(contenido)
    return vector_caracteres


def contar_frecuencias(vec):
    """
    Cuenta la frecuencia de caracteres y los indexa

    Parámetros:
    vec (list): El vector de caracteres

    Retorna:
    list: El vector de caracteres unicos
    list: El vector con la cantidad de apariciones
    """
    
    #cuenta las apariciones de cada caracter
    frecuencias = Counter(vec)
    caracteres_unicos = sorted(frecuencias.keys())
    vector = [frecuencias[char] for char in caracteres_unicos]

    return caracteres_unicos, vector


def crea_vec_probabilidades(frecuencias):
    """
    Obtiene el vector de probabilidades

    Parámetros:
    frecuencias (list): El vector de frecuencias

    Retorna:
    list: El vector de probabilidades
    """

    total = sum(frecuencias)
    vec = [elemento / total for elemento in frecuencias]
    return vec
    
def crea_matriz_trans(vec, caracteres):
    """
    Crea la matriz de probabilidades de transición

    Parámetros:
    vec (list): El vector con los símbolos de la fuente
    caracteres (list): El vector con los caracteres únicos

    Retorna:
    numpy.ndarray: La matriz de transición
    """


    n = len(caracteres)
    #indexea los caracteres
    char_index = {char: idx for idx, char in enumerate(caracteres)}
    
    # Inicializa la matriz de transición con ceros
    matriz_transicion = np.zeros((n, n), dtype=float)
    
    # Contar las transiciones entre caracteres
    for (current_char, next_char) in zip(vec[:-1], vec[1:]):
        i = char_index[current_char]
        j = char_index[next_char]
        matriz_transicion[j, i] += 1

    for j in range(n):
        columna_suma = matriz_transicion[:,j].sum()
        if columna_suma > 0:
            matriz_transicion[:,j] /= columna_suma
    
    return matriz_transicion

def calcular_entropia(vec_probabilidades):
    """
    Calcula la entropia haciendo la sumatoria en el for
    
    Parámetros:
    vec_probabilidades (list): El vector de probabilidades de los símbolos

    Retorna:
    float: La entropía de la fuente
    """
    suma = 0

    for i in range(len(vec_probabilidades)):
        suma += vec_probabilidades[i]*np.log2(1/vec_probabilidades[i])

    return suma

def calcular_entropia_condicional(matriz_transicion, vector_estacionario):
    """
    Calcula la entropía condicional de una fuente de Markov de orden 1

    Parámetros:
    matriz_transicion (float) : La matriz con las probabilidades condicionales
    vector_estacionario (float) : El vector estacionario ya equilibrado

    Retorna:
    float: La entropía condicional de la fuente
    """

    entropia_condicional = 0

    for j in range(len(vector_estacionario)):
        probabilidades = matriz_transicion[:, j]
        
        # Evitar problemas con logaritmo de 0
        probabilidades = probabilidades[probabilidades> 0]
        
        # Sumar el cálculo de la entropía condicional
        entropia_condicional += np.sum(probabilidades * np.log2(1 / probabilidades)) * vector_estacionario[j]
    
    return entropia_condicional

def extension_de_la_fuente(N, caracteres, probabilidades):
    """
    Calcula todas las posibles secuencias de longitud N y sus respectivas probabilidades
    según las probabilidades de los caracteres de la fuente

    Parámetros:
    N (int): El orden de la extensión de la fuente (longitud de las secuencias)
    caracteres (list): El vector de caracteres únicos de la fuente
    probabilidades (list): El vector de probabilidades correspondiente a cada carácter

    Retorna:
    None: Imprime las secuencias y sus probabilidades
    """
    
    # Crear un diccionario que asocia cada carácter con su probabilidad
    prob_dict = dict(zip(caracteres, probabilidades))

    # Generar todas las combinaciones posibles de longitud N
    sequences = list(product(caracteres, repeat=N))

    # Calcular la probabilidad de cada secuencia
    sequence_probabilities = [
        (seq, product(prob_dict[char] for char in seq))
        for seq in sequences
    ]

    # Mostrar los resultados
    for seq, prob in sequence_probabilities:
        print(f"Secuencia: {''.join(seq)}, Probabilidad: {prob:.5f}")

def vector_estacionario_iterativo(matriz, cantidad):
    """"
    Calcula el vector estacionario mediante cierta cantidad de iteraciones ingresada por parametro

    Parámetros:
    matriz (double): La matriz de probabilidades
    cantidad (int): El número de iteraciones a realizar

    Retorna:
    double: El vector final
    """

    n = len(matriz)
    vector = [1/n for _ in range(n)]
    
    for i in range(cantidad):
        vector = np.dot(matriz, vector) 

    return vector

def es_memoria_nula(entropia, entropia_c, tol):
    """"
    Verifica si se trata de una fuente de memoria nula

    Parámetros:
    entropia (float): La entropía de la fuente
    entropia_c (float): La entropía condicional de la fuente
    tol (float): La tolerancia para comparar las dos fuentes

    Retorna:
    bool: True si se trata de una fuente de memoria nula, False caso contrario.

    """
    valor = abs(entropia - entropia_c);

    return valor < tol

def crear_vector_estacionario(matriz):
    """
    Obtiene el vector estacionario

    Parámetros:
    matriz (numpy.ndarray): La matriz de transición de la fuente

    retorna:
    numpy.ndarray: El vector estacionario
    """

    n = len(matriz)

    # Crea la matriz identidad
    identidad = np.eye(n)

    # Resta la matriz identidad a la matriz de transición
    matriz -= identidad

    # Agregar la ecuación de normalización: V1 + V2 + ... + Vn = 1
    ecuacion_normalizacion = np.ones((1, n))
    
    # Crear la nueva matriz del sistema agregando la ecuación de normalización
    matriz = np.vstack([matriz, ecuacion_normalizacion])

    # Crea el vector independiente para despues realizar el sistema de ecuaciones con la libreria del return
    vector_independiente = np.zeros(n + 1)
    vector_independiente[n] = 1

    return np.linalg.lstsq(matriz, vector_independiente, rcond=None)[0]

# Obtener el nombre del archivo
nombre_archivo = sys.argv[0]

# Obtener el primer argumento (si existe)
if len(sys.argv) > 1:
    N = sys.argv[1]
    # nombre_archivo = 'tp1_samples/tp1_sample0.txt'
    vec = leer_archivo(nombre_archivo)
    caracteres, frecuencias = contar_frecuencias(vec)

    vec_probabilidades = crea_vec_probabilidades(frecuencias)

    matriz_transicion = crea_matriz_trans(vec, caracteres)

    print("a) Matriz: \n", matriz_transicion)

    entropia = calcular_entropia(vec_probabilidades)
    vector_iterativo = vector_estacionario_iterativo(matriz_transicion, 30) # 30 es la cant de iteraciones
    entropia_c = calcular_entropia_condicional(matriz_transicion, vector_iterativo)

    resultado = es_memoria_nula(entropia, entropia_c, 0.005) # 0.005 es el margen maximo de error

    if(resultado):
        print("b) La fuente es de memoria nula")
        print("c) Vector de probabilidades: \n", vec_probabilidades)
        extension_de_la_fuente(N, vec_probabilidades)
        print("e) Entropía: ", entropia)
    else:
        print("b) La fuente es de memoria no nula")
        print("d) Vector estacionario: ", crear_vector_estacionario(matriz_transicion))
        print("e) Entropía: ", entropia_c)
else:
    print("No se proporcionó un nombre")