from collections import Counter
import numpy as np
from itertools import product

def leer_archivo(nombre_archivo):
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
    #cuenta las apariciones de cada caracter
    frecuencias = Counter(vec)
    caracteres_unicos = sorted(frecuencias.keys())
    vector = [frecuencias[char] for char in caracteres_unicos]

    return caracteres_unicos, vector


def crea_vec_probailidades(frecuencias):
    vec = {}
    total = sum(frecuencias)
    vec = frecuencias
    vec = [elemento / total for elemento in vec]
    return vec
    
def crea_matriz_trans(vec, caracteres):
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

def entropia(vec_probabilidades):
    #funcion que calcula la entropia haciendo la sumatoria en el for
    suma = 0

    for i in range(len(vec_probabilidades)):
        suma += vec_probabilidades[i]*np.log2(1/vec_probabilidades[i])

    return suma

def extension_de_la_fuente(caracteres,probabilidades):
    

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
    # matriz es la de probabilidades
    # cantidad es el numero de interacciones a realizar

    vector = np.array([1/3, 1/3, 1/3])
    for i in range(cantidad):
        vector = np.dot(matriz, vector) 

    return vector

def Rango_Nulo(vec_E,vec_I,valor):
    
    vec = vec_E-vec_I
    vec = np.abs(vec)

    if np.all(vec < valor):
        print("tiene memoria no nula")
    else:
        print("tiene memoria nula")

#nombre_archivo = 'D:/universidad/teoriainfo/tp1/.venv/tp1/tp1_sample3.txt'
#vec = leer_archivo(nombre_archivo)
vec = "BBAAACCAAABCCCAACCCBBACCAABBAA"
caracteres,frecuencias = contar_frecuencias(vec)
vec_probabilidades = crea_vec_probailidades(frecuencias)
print("\n vector estacionario: \n",vec_probabilidades,"\n")
matriz_transicion = crea_matriz_trans(vec,caracteres)
extension_de_la_fuente(caracteres,vec_probabilidades)
print("\n matriz: \n",matriz_transicion)
print("\n entropia :",entropia(vec_probabilidades),"\n")
vector_iterativo = Vector_estacionario_iterativo(matriz_transicion,3) # 3 es la cat de iteraciones
print("\n Vector iterativo con 3 pasos: ",vector_iterativo)
