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

def leer_arch_y_agrega_paridad(archivo, N):
    matrices = []  # Lista para almacenar las matrices generadas
    matriz_actual = np.zeros((N + 1, N + 1), dtype=int)  # Inicializar la matriz de ceros con una fila y columna extra
    
    with open(archivo, 'rb') as f:
        byte = f.read(1)
        bit_index = 0  # Índice para rastrear la posición del bit en la matriz actual

        while byte:
            # Convertir el byte a una secuencia de bits
            for bit in f'{ord(byte):08b}':
                # Calcular la posición de fila y columna en la matriz actual
                fila = (bit_index + 1) % (N + 1)  # La primera fila está ocupada por ceros
                columna = bit_index // N
                
                # Insertar el bit en la matriz actual
                matriz_actual[fila, columna] = int(bit)
                
                # Incrementar el índice de bits
                bit_index += 1
                
                # Si completamos una matriz N x N, la agregamos a la lista y reiniciamos
                if bit_index >= N * N:
                    # Modificar la columna adicional con valores alternos de 0 y 1
                    for i in range(N + 1):
                        matriz_actual[i, N] = i % 2  # Columna adicional con 0 y 1 intercalados
                    
                    matrices.append(matriz_actual)
                    matriz_actual = np.zeros((N + 1, N + 1), dtype=int)  # Nueva matriz vacía
                    bit_index = 0  # Reiniciar el índice de bits para la nueva matriz
            
            # Leer el siguiente byte
            byte = f.read(1)
    
    # Si hay una matriz incompleta (no llena pero con algunos bits), agregarla
    if bit_index > 0:
        # Modificar la columna adicional con valores alternos de 0 y 1
        for i in range(N + 1):
            matriz_actual[i, N] = i % 2  # Columna adicional con 0 y 1 intercalados
        matrices.append(matriz_actual)
    
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

ruta_archivo = "C:/teoria-de-la-info/TP-4/tp4_samples/tp4_sample0_sent.bin"
contenido_binario = leer_archivo(ruta_archivo)
caracteres_unicos = obtener_caracteres_unicos(contenido_binario)
vector_probabilidades = calcular_probabilidades(contenido_binario, caracteres_unicos)
entropia = calcular_entropia(vector_probabilidades)
aux = leer_arch_y_agrega_paridad(ruta_archivo,4)
print(aux[0])
print(f"a)Entropía: {entropia:.6f} binits")
ruta_archivo = "C:/teoria-de-la-info/TP-4/tp4_samples/tp4_sample0_recv1.bin"
contenido_binario_recibido = leer_archivo(ruta_archivo)
contenido_bits_recibido = convertir_a_bits(contenido_binario_recibido)
#matriz_probabilidades_C = calcular_matriz_probabilidad(contenido_binario_enviado,contenido_binario_recibido)