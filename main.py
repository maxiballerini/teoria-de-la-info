from collections import Counter
import numpy as np
from itertools import product

def leer_archivo(nombre_archivo):
    """
    Funcion para leer un archivo y guardar su contenido en un array

    Retorna:
    cadena de caracteres
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
    Funcion para contar la frecuencia de caracteres e indexarlos

    Retorna:
    vector de caracteres unicos y el vector con su cantidad de apariciones
    """
     
    #cuenta las apariciones de cada caracter
    frecuencias = Counter(vec)
    caracteres_unicos = sorted(frecuencias.keys())
    vector = [frecuencias[char] for char in caracteres_unicos]

    return caracteres_unicos, vector


def crea_vec_probabilidades(frecuencias):
    """
    Funcion para obtener el vector de probabilidades

    Retorna:
    vector de probabilidades
    """

    vec = {}
    total = sum(frecuencias)
    vec = frecuencias
    vec = [elemento / total for elemento in vec]
    return vec
    
def crea_matriz_trans(vec, caracteres):
    """
    Funcion para crear la matriz de probabilidades de transicion

    Retorna:
    matriz transicion
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
    """""
    funcion que calcula la entropia haciendo la sumatoria en el for
    
    Retorna:
    float: entropia
    """
    suma = 0

    for i in range(len(vec_probabilidades)):
        suma += vec_probabilidades[i]*np.log2(1/vec_probabilidades[i])

    return suma

def calcular_entropia_condicional(matriz_transicion, vector_estacionario):
    
    entropia_condicional = 0

    for j in range(len(vector_estacionario)):
        probabilidades = matriz_transicion[:, j]
        
        # Evitar problemas con logaritmo de 0
        probabilidades = probabilidades[probabilidades> 0]
        
        # Sumar el cálculo de la entropía condicional
        entropia_condicional += np.sum(probabilidades * np.log2(1 / probabilidades)) * vector_estacionario[j]
    
    return entropia_condicional

def extension_de_la_fuente(caracteres, probabilidades):
    

    # Crear un diccionario que asocia los símbolos con sus probabilidades
    prob_dict = dict(zip(caracteres, probabilidades))

    # Generar todas las combinaciones posibles de longitud 3
    sequences = list(product(caracteres, repeat=len(caracteres)))

    # Calcular la probabilidad de cada secuencia
    sequence_probabilities = [(seq, prob_dict[seq[0]] * prob_dict[seq[1]] * prob_dict[seq[2]]) for seq in sequences]

    # Mostrar los resultados
    for seq, prob in sequence_probabilities:
        print(f"Secuencia: {''.join(seq)}, Probabilidad: {prob:.5f}")

def Vector_estacionario_iterativo(matriz,cantidad):
    """"
    funcion para calcular el vector iterativo en una cantidad ingresada por parametros

    matriz es la de probabilidades
    cantidad es el numero de interacciones a realizar

    Retorna:
    vector final
    """

    n = len(matriz)
    vector = [1/n for _ in range(n)]
    
    for i in range(cantidad):
        vector = np.dot(matriz, vector) 

    return vector

def es_memoria_nula(entropia_m, entropia_c, tol):
    """"
    funcion para saber si la memoria de la fuente es nula
    """
    valor = abs(entropia_m - entropia_c);
    print(valor)

    if valor < tol:
        return True
    else:
        return False

def crear_vector_estacionario(matriz):
    """"
    funcion para obtener el vector estacionario

    retorna:
    vector estacionario
    """

    # tamaño de la matriz cuadrada
    n = len(matriz)
    
    # realiza la resta con la matriz de probabilidades y una matriz de identidad
    for i in range(n):
        for j in range(n):
            if i == j:
                matriz[i,j] -=1
    
    # Agregar la ecuación de normalización: V1 + V2 + ... + Vn = 1
    ecuacion_normalizacion = np.ones((1, n))
    
    # Crear la nueva matriz del sistema agregando la ecuación de normalización
    matriz = np.vstack([matriz, ecuacion_normalizacion])

    # crea el vector independiente para despues realizar el sistema de ecuaciones con la libreria del return
    vector_independiente = np.zeros(n + 1)
    vector_independiente[n] = 1

    return np.linalg.lstsq(matriz, vector_independiente, rcond=None)[0]

nombre_archivo = 'tp1_samples/tp1_sample0.txt'
vec = leer_archivo(nombre_archivo)
caracteres, frecuencias = contar_frecuencias(vec)

vec_probabilidades = crea_vec_probabilidades(frecuencias)

matriz_transicion = crea_matriz_trans(vec, caracteres)

print("a) Matriz: \n", matriz_transicion)

entropia_m = calcular_entropia(vec_probabilidades)
vector_iterativo = Vector_estacionario_iterativo(matriz_transicion, 30) # 30 es la cant de iteraciones
entropia_c = calcular_entropia_condicional(matriz_transicion, vector_iterativo)

resultado = es_memoria_nula(entropia_m, entropia_c, 0.005) # 0.005 es el margen maximo de error
if(resultado):
    print("b) La fuente es de memoria nula")
    print("c) Vector de probabilidades: \n", vec_probabilidades)
    extension_de_la_fuente(caracteres, vec_probabilidades)
    print("e) Entropía: ", entropia_m)
else:
    print("b) La fuente es de memoria no nula")
    print("d) Vector estacionario: ", crear_vector_estacionario(matriz_transicion))
    print("e) Entropía: ", entropia_c)