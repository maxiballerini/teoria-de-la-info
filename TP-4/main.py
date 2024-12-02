import sys
import numpy as np
import math
from collections import Counter
from itertools import product

def leer_archivo(nombre_archivo):
    # Abrir el archivo en modo lectura binaria
    with open(nombre_archivo, 'rb') as archivo:
        # Leer el contenido del archivo
        contenido = archivo.read()
        
    # Convertir el contenido en bits (1s y 0s)
    bits = ''.join(format(byte, '08b') for byte in contenido)
    
    return bits

def agrega_paridad(contenido, N):
    matrices = []  # Lista para almacenar las matrices generadas
    matriz_datos = np.zeros((N, N), dtype=int)  # Inicializar la matriz de ceros con una fila y columna extra
    bit_index = 0  # Índice para rastrear la posición del bit en la matriz actual
    
    for bit in contenido:
        columna = bit_index // N  # Determina la columna por el índice
        fila = bit_index % N  # Determina la fila dentro de la columna
        matriz_datos[fila, columna] = int(bit)  # Coloca el bit en la matriz
        bit_index += 1
        
        # Si completamos una matriz N x N, la agregamos a la lista y reiniciamos
        if bit_index >= N * N:

            matriz_paridad = np.zeros((N + 1, N + 1), dtype=int) # Crear matriz extendida
            matriz_paridad[:N, :N] = matriz_datos # Copiar datos a la matriz extendida

            for i in range(N):
                matriz_paridad[i, N] = matriz_datos[:, i].sum() % 2 # Calculo de VRC
                matriz_paridad[N, i] = matriz_datos[i, :].sum() % 2 # Calculo de LRC
            matriz_paridad[N, N] = matriz_datos.sum() % 2 # Calculo de paridad cruzada que comprueba paridades
            
            matrices.append(matriz_paridad)
            matriz_datos = np.zeros((N, N), dtype=int)  # Nueva matriz vacía
            bit_index = 0  # Reiniciar el índice de bits para la nueva matriz
    
    if bit_index > 0:
        matriz_paridad = np.zeros((N + 1, N + 1), dtype=int)
        matriz_paridad[:N, :N] = matriz_datos  # Copiar datos a la matriz extendida
        for i in range(N):
            matriz_paridad[i, N] = matriz_datos[:, i].sum() % 2 # Calculo de VRC
            matriz_paridad[N, i] = matriz_datos[i, :].sum() % 2 # Calculo de LRC
        matriz_paridad[N, N] = matriz_datos.sum() % 2 # Calculo de paridad cruzada que comprueba paridades
        matrices.append(matriz_paridad)
    
    vector_lineal = []
    for matriz in matrices:
        vector_lineal.extend([int(x) for x in matriz.flatten(order='C')])
    
    return vector_lineal

def calcular_matriz_probabilidad(bits_transmitidos, bits_recibidos):
    # Inicializar la matriz de probabilidades (2x2)
    matriz_probabilidad = np.zeros((2, 2))
    
    # Asegúrate de que las secuencias de bits sean de la misma longitud
    assert len(bits_transmitidos) == len(bits_recibidos), "Las secuencias deben ser del mismo tamaño."
    
    # Contar las transiciones
    for bit_transmitido, bit_recibido in zip(bits_transmitidos, bits_recibidos):
        matriz_probabilidad[int(bit_transmitido)][int(bit_recibido)] += 1
    
    # Normalizar las filas para obtener las probabilidades
    for i in range(2):
        suma_fila = np.sum(matriz_probabilidad[i])
        if suma_fila > 0:
            matriz_probabilidad[i] /= suma_fila
    
    return matriz_probabilidad

def calcular_probabilidades(contenido):
    conteo_total = len(contenido)
    if conteo_total == 0:  # Manejar el caso de un vector vacío
        return [0, 0]
    
    # Contar las ocurrencias de 0 y 1
    prob_0 = contenido.count(0) / conteo_total
    prob_1 = contenido.count(1) / conteo_total
    
    return [prob_0, prob_1]

def calcular_entropia(vec_probabilidades):
    suma = 0
    for prob in vec_probabilidades:
        if prob > 0:  # Evitar problemas con log(0)
            suma += prob * np.log2(1 / prob)
    return suma

def calcular_vector_B(vector_a, matriz_condicional):

    vector_a = np.array(vector_a) 
    matriz_condicional = np.array(matriz_condicional)
    
    # Producto de P(ai) con cada columna de P(bj | ai)
    vector_b = np.dot(vector_a, matriz_condicional)  # Multiplicación de matriz por vector
    
    return vector_b.tolist() 
def calcular_probabilidades_conjuntas(vector_a, matriz_condicional):

    vector_a = np.array(vector_a) 
    matriz_condicional = np.array(matriz_condicional) 

    # Calcular P(ai, bj) = P(ai) * P(bj | ai)
    matriz_conjunta = matriz_condicional * vector_a[:, np.newaxis] 

    return matriz_conjunta.tolist()

def calcular_matriz_condicional(matriz_conjunta, probs_b):

    matriz_condicional = []  # Inicializamos la matriz de resultados

    for i in range(len(matriz_conjunta)):  # Iteramos sobre las filas
        fila_condicional = []  # Fila para almacenar los valores condicionales
        for j in range(len(matriz_conjunta[i])):  # Iteramos sobre las columnas
            if probs_b[j] > 0:  # Verificamos que P(bj) sea mayor a 0
                valor_condicional = matriz_conjunta[i][j] / probs_b[j]
            else:  # Si P(bj) es 0, definimos un valor muy pequeño para evitar división por cero
                valor_condicional = 0
            fila_condicional.append(valor_condicional)  # Añadimos el valor a la fila
        matriz_condicional.append(fila_condicional)  # Añadimos la fila a la matriz

    return matriz_condicional

def bits_a_vector_de_matrices(bits_recived, N):
    total_bits = len(bits_recived)
    bits_por_matriz = N * N
    # Convertir la cadena de bits a una lista de enteros (0 o 1)
    bits = [int(b) for b in bits_recived]

    # Crear las matrices N x N y almacenarlas en un vector
    vector_de_matrices_recived = []
    for i in range(0, total_bits, bits_por_matriz):
        matriz_lineal = np.array(bits[i:i + bits_por_matriz])
        # Reorganizar los datos en una matriz N x N llenada por columnas
        matriz = matriz_lineal.reshape(N, N, order='F')
        vector_de_matrices_recived.append(matriz)

    return vector_de_matrices_recived

def verificar_mensajes(array_matrices):
    # Contadores de resultados
    correctos = 0
    corregibles = 0
    erroneos = 0
    # Iterar sobre las matrices recibidas
    for matriz in array_matrices:
        N = matriz.shape[0] # Tamaño de la matriz con bits de paridad

        # Verificar paridad por filas 
        errores_filas = 0
        for i in range(N):
            errores_filas += sum(matriz[i, :N]) % 2

        # Verificar paridad por columnas
        errores_columnas = 0
        for j in range(N):
            errores_columnas += sum(matriz[:N, j]) % 2
        if errores_filas == 0 and errores_columnas == 0:
            correctos += 1  # No hay errores
        elif errores_filas == 1 and errores_columnas == 1:
            corregibles += 1  # Un error en fila, un error en columna
        else:
            erroneos += 1  # Más de dos errores

    return correctos, corregibles, erroneos

def calcular_entropia_a_priori(probs):
    entropia = 0
    for p in probs:
        if p > 0:  # Evitar logaritmo de 0
            entropia +=p * (math.log2(1 / p))  # Fórmula de entropía
    return entropia

def calcular_entropias_a_posteriori(matriz_probs):
    entropias = []  # Lista para almacenar las entropías a posteriori de cada conjunto

    for j in range(2):  # Para cada símbolo de salida bj
        entropia = 0
        for i in range(2):  # Para cada símbolo de entrada ai
            prob = matriz_probs[i][j]
            if prob > 0:  # Evitar logaritmo de 0
                entropia += prob * (math.log2(1 / prob))  # Fórmula de entropía
        entropias.append(entropia)  # Añadir la entropía calculada para este conjunto

    return entropias

def calcular_equivocacion(matriz_prob_conjunta, matriz_condicional):
    equivocacion = 0

    for i in range(len(matriz_prob_conjunta)):  # Iterar sobre los eventos de A
        for j in range(len(matriz_prob_conjunta[0])):  # Iterar sobre los eventos de B
            p_ab = matriz_prob_conjunta[i][j]
            p_a_dado_b = matriz_condicional[i][j]
            if p_a_dado_b > 0:  # Evitar logaritmo de 0
                equivocacion += p_ab * math.log2(1 / p_a_dado_b)  # Sumar término de la fórmula

    return equivocacion  

def calcular_perdida(matriz_condicional, matriz_conjunta):
    perdida = 0

    for i in range(len(matriz_conjunta)):  # Para cada símbolo de entrada (a)
        for j in range(len(matriz_conjunta[0])):  # Para cada símbolo de salida (b)
            p_ab = matriz_conjunta[i][j]  # P(a, b)
            p_b_a = matriz_condicional[i][j]  # P(b|a)
            if p_ab > 0 and p_b_a > 0:  # Evitar logaritmos de 0
                perdida += p_ab * math.log2(1 / p_b_a)
    return perdida


if len(sys.argv) != 4:
    print("Uso: python main.py <sent> <received> <N>")

else:
    archivo_sent = sys.argv[1]
    archivo_received = sys.argv[2]
    N = int(sys.argv[3])

    contenido_enviado = leer_archivo(archivo_sent)
    # Se almacena nuevamente el contenido del archivo en una lista pero con los bits de paridad añadidos
    contenido_enviado = agrega_paridad(contenido_enviado, N)
    contenido_recibido = leer_archivo(archivo_received)
    vec_probabilidadA = calcular_probabilidades(contenido_enviado)
    print(f"Vector probabilidades: {vec_probabilidadA}")
    entropia_de_la_fuente = calcular_entropia(vec_probabilidadA)


    print(f"a) La entropia de la fuente es: {entropia_de_la_fuente:.6f} binits")
    matriz_canal = calcular_matriz_probabilidad(contenido_enviado, contenido_recibido)
    print("c) La matriz del canal es: \n", matriz_canal)
    vector_probabilidadesB = calcular_vector_B(vec_probabilidadA, matriz_canal)
    matriz_conjunta = calcular_probabilidades_conjuntas(vec_probabilidadA, matriz_canal)
    matriz_posteriori = calcular_matriz_condicional(matriz_conjunta, vector_probabilidadesB)

    matrices_received = bits_a_vector_de_matrices(contenido_recibido, N + 1)
    mensajes_correctos, mensajes_erroneos, mensajes_corregibles = verificar_mensajes(matrices_received)
    print(f"d) Cantidad de enviados correctamente: {mensajes_correctos}")
    print(f"Cantidad de mensajes erróneos: {mensajes_erroneos}")
    print(f"Cantidad de mensajes corregidos: {mensajes_corregibles}")

    entropia_a_prioriA = calcular_entropia_a_priori(vec_probabilidadA)
    entropias_posterioriA = calcular_entropias_a_posteriori(matriz_posteriori)
    print(f"e) Entropía a priori H(A): {entropia_a_prioriA:.6f} binits")
    print(f"Entropías a posteriori: H(A/0) = {entropias_posterioriA[0]:.6f} binits , H(A/1) = {entropias_posterioriA[1]:.6f} binits")


    equivocacion = calcular_equivocacion(matriz_conjunta, matriz_posteriori)
    perdida = calcular_perdida(matriz_canal, matriz_conjunta)
    print(f"La información mutua es: {entropia_a_prioriA - equivocacion:.4f}")
    print(f"El ruido es: {equivocacion:4f}")
    print(f"La perdida es: {perdida:4f}") 


