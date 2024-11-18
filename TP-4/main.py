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

def obtener_caracteres_unicos(contenido):
    # Obtiene una lista de caracteres únicos en el contenido (en este caso, los bits únicos)
    return list(set(contenido))

def calcular_probabilidades(contenido, caracteres_unicos):
    # Cuenta las ocurrencias de cada bit (1 o 0)
    conteo_total = len(contenido)
    contador = Counter(contenido)
    
    # Calcula la probabilidad de cada bit único (1 o 0)
    probabilidades = [contador[caracter] / conteo_total for caracter in caracteres_unicos]
    return probabilidades
def calcular_entropia(vec_probabilidades):
    suma = 0
    for i in range(len(vec_probabilidades)):
        suma += vec_probabilidades[i]*np.log2(1/vec_probabilidades[i])

    return suma

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

def genera_matrices_paridad(contenido, N):
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
    
    # Si hay una matriz incompleta (no llena pero con algunos bits), agregarla
    if bit_index > 0:
        matriz_paridad = np.zeros((N + 1, N + 1), dtype=int)
        matriz_paridad[:N, :N] = matriz_datos  # Copiar datos a la matriz extendida
        for i in range(N):
            matriz_paridad[i, N] = matriz_datos[:, i].sum() % 2 # Calculo de VRC
            matriz_paridad[N, i] = matriz_datos[i, :].sum() % 2 # Calculo de LRC
        matriz_paridad[N, N] = matriz_datos.sum() % 2 # Calculo de paridad cruzada que comprueba paridades
        matrices.append(matriz_paridad)
    
    return matrices

def convertir_a_bits(contenido):
    # Convertir el contenido binario a una lista de bits
    bits = []
    for byte in contenido:
        # Convertir cada byte a su representación binaria de 8 bits
        bits.extend([int(bit) for bit in f'{byte:08b}'])
    return bits

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

def extraer_bits_matrices(matrices_received, N):
    # Lista para almacenar los bits extraídos
    contenido_bits_recibido = []

    # Iterar sobre las matrices recibidas
    for matriz in matrices_received:
        # Validar que la matriz sea de tamaño N x N
        if matriz.shape[0] == N and matriz.shape[1] == N:
            # Recorrer hasta la penúltima columna y fila
            for j in range(N - 1):  # Recorrer columnas
                for i in range(N - 1):  # Recorrer filas
                    contenido_bits_recibido.append(matriz[i, j])
                    
    return contenido_bits_recibido

def verificar_mensajes(array_matrices1, array_matrices2):
    def obtener_bits_paridad(matriz):
        N = matriz.shape[0] - 1  # Tamaño real de la matriz sin la fila y columna de paridad
        # Obtener bits de paridad
        paridad_lrc = matriz[N, :-1]  # Última fila sin el bit de paridad cruzada
        paridad_vrc = matriz[:-1, N]  # Última columna sin el bit de paridad cruzada
        paridad_cruzada = matriz[N, N]  # Bit de paridad cruzada
        return paridad_lrc, paridad_vrc, paridad_cruzada

    # Contadores de resultados
    correctos = 0
    corregibles = 0
    erroneos = 0

    # Iterar sobre los pares de matrices
    for matriz1, matriz2 in zip(array_matrices1, array_matrices2):
        # Obtener los bits de paridad de ambas matrices
        lrc1, vrc1, cruzada1 = obtener_bits_paridad(matriz1)
        lrc2, vrc2, cruzada2 = obtener_bits_paridad(matriz2)

        # Comparar bits de paridad
        errores = 0
        if not np.array_equal(lrc1, lrc2):
            errores += 1
        if not np.array_equal(vrc1, vrc2):
            errores += 1
        if cruzada1 != cruzada2:
            errores += 1

        # Determinar el estado del mensaje
        if errores == 0:
            correctos += 1
        elif errores == 1 or (errores == 2 and cruzada1 != cruzada2):
            corregibles += 1
        else:
            erroneos += 1

    # Retornar los conteos
    return correctos, corregibles, erroneos

def calcular_entropias_a_priori(probs, N):
    entropia = 0
    for i in range(N):
        for p in probs:
            if p > 0:  # Evitar logaritmo de 0
                entropia +=p * (math.log2(1 / p))  # Fórmula de entropía
    return entropia

def calcular_entropias_a_posteriori(matriz_probs, N):
    entropias = []  # Lista para almacenar las entropías a posteriori de cada conjunto

    for j in range(len(matriz_probs[0])):  # Para cada símbolo de salida bj
        entropia = 0
        for i in range(N):  # Para cada símbolo de entrada ai
            prob = matriz_probs[i][j]
            if prob > 0:  # Evitar logaritmo de 0
                entropia -= prob * math.log2(prob)  # Fórmula de entropía
        entropias.append(entropia)  # Añadir la entropía calculada para este conjunto

    return entropias   

if len(sys.argv) != 4:
    print("Uso: python main.py <sent> <received> <N>")
else:
    # Guardo los parametros
    archivo_sent = sys.argv[1]
    archivo_received = sys.argv[2]
    N = int(sys.argv[3])

    contenido_binario_enviado = leer_archivo(archivo_sent)
    caracteres_unicos = obtener_caracteres_unicos(contenido_binario_enviado)
    vector_probabilidades = calcular_probabilidades(contenido_binario_enviado, caracteres_unicos)
    print(vector_probabilidades)
    entropia = calcular_entropia(vector_probabilidades)
    print(f"a)Entropía: {entropia:.6f} binits")

    matrices_sent = genera_matrices_paridad(contenido_binario_enviado, N) 
    contenido_binario_recibido = leer_archivo(archivo_received)
    matrices_received = bits_a_vector_de_matrices(contenido_binario_recibido, N + 1)

    contenido_bits_recibido = extraer_bits_matrices(matrices_received, N + 1)
    matriz_probabilidades = calcular_matriz_probabilidad(contenido_binario_enviado, contenido_bits_recibido)
    print(f"c) {matriz_probabilidades}")

    mensajes_correctos, mensajes_erroneos, mensajes_corregibles = verificar_mensajes(matrices_sent, matrices_received)
    print(f"d) Cantidad de enviados correctamente: {mensajes_correctos}")
    print(f"Cantidad de mensajes erróneos: {mensajes_erroneos}")
    print(f"Cantidad de mensajes corregidos: {mensajes_corregibles}")

    entropia_a_priori = calcular_entropias_a_priori(vector_probabilidades, N)
    entropias_posteriori = calcular_entropias_a_posteriori(matriz_probabilidades, N)
    print(f"Entropía a priori: {entropia_a_priori:.6f} binits")
    print(f"Entropías a posteriori: H(0) = {entropias_posteriori[0]:.6f} binits , H(1) = {entropias_posteriori[1]:.6f} binits")

