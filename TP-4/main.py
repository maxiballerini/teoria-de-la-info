import sys
import numpy as np
from collections import Counter
from itertools import product

def leer_archivo(nombre_archivo):
    # Abrir el archivo en modo lectura
    with open(nombre_archivo, 'rb') as archivo:
        # Leer el contenido del archivo
        contenido = archivo.read()  
        # Agregar cada carácter del contenido a la lista
    return contenido


def obtener_caracteres_unicos(contenido):
    # Obtiene una lista de caracteres únicos en el contenido
    return list(set(contenido))

def calcular_probabilidades(contenido, caracteres_unicos):
    # Cuenta las ocurrencias de cada byte en el contenido
    conteo_total = len(contenido)
    contador = Counter(contenido)
    
    # Calcula la probabilidad de cada carácter único
    probabilidades = [contador[caracter] / conteo_total for caracter in caracteres_unicos]
    return probabilidades

def calcular_entropia(vec_probabilidades):
    suma = 0
    for i in range(len(vec_probabilidades)):
        suma += vec_probabilidades[i]*np.log2(1/vec_probabilidades[i])

    return suma

def genera_matrices_paridad(contenido, N):
    matrices = []  # Lista para almacenar las matrices generadas
    matriz_datos = np.zeros((N, N), dtype=int)  # Inicializar la matriz de ceros con una fila y columna extra
    bit_index = 0  # Índice para rastrear la posición del bit en la matriz actual
    
    for byte in contenido:
        for bit in f'{byte:08b}':
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
        matriz_probabilidad[bit_transmitido][bit_recibido] += 1
    
    # Normalizar las filas para obtener las probabilidades
    for i in range(2):
        suma_fila = np.sum(matriz_probabilidad[i])
        if suma_fila > 0:
            matriz_probabilidad[i] /= suma_fila
    
    return matriz_probabilidad

if len(sys.argv) != 4:
    print("Uso: python tpi4.py <sent> <received> <N>")
else:
    archivo_sent = sys.argv[1]
    archivo_received = sys.argv[2]
    N = int(sys.argv[3])
    contenido_binario_enviado = leer_archivo(archivo_sent)
    caracteres_unicos = obtener_caracteres_unicos(contenido_binario_enviado)
    vector_probabilidades = calcular_probabilidades(contenido_binario_enviado, caracteres_unicos)
    entropia = calcular_entropia(vector_probabilidades)
    matrices = genera_matrices_paridad(contenido_binario_enviado, N) # Las matrices generadas tienen los bits de paridad en las fila N+1 y columna N+1
    # Sacar el comentario para ver como queda una matriz
    # print(matrices[0]) 
    print(f"a)Entropía: {entropia:.6f} binits")
    contenido_binario_recibido = leer_archivo(archivo_received)
    contenido_bits_recibido = convertir_a_bits(contenido_binario_recibido)
    # matriz_probabilidades = calcular_matriz_probabilidad(contenido_binario_enviado, contenido_binario_recibido)
    # print(matriz_probabilidades)