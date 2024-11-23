import os
import heapq
from collections import Counter
import pickle
import sys
import time
import math

def abrir_archivo(nombre_archivo):
    # Abriendo un archivo de imagen en modo binario
    with open(nombre_archivo, "rb") as archivo:
        contenido_binario = archivo.read()  # Lee todo el contenido del archivo como bytes
    return contenido_binario

def obtener_probabilidades(contenido):
    #Función que obtiene las probabilidades de cada símbolo(byte), devuelve un diccionario (byte-probabilidad)

    total = len(contenido)
    conteo_bytes = Counter(contenido) # Contador que tiene cada byte y cuantas veces aparece
    res = {}
    for byte_unico, frec in conteo_bytes.items():
        res[byte_unico] = float(frec) / total
    #res = dict(sorted(res.items(), key=lambda item: item[1], reverse=False))
    return res

def obtener_arbol_Huffman(probabilidades):
    fila_prioridad = []

    for simbolo,probabilidad in probabilidades.items():
        fila_prioridad.append((probabilidad, 0, simbolo))
    
    fila_prioridad.sort()

    while len(fila_prioridad) > 1:
        menos_probable = fila_prioridad.pop(0) 
        seg_menos_probable = fila_prioridad.pop(0) 
        
        nuevo_nodo = (menos_probable[0] + seg_menos_probable[0], 
                    max(menos_probable[1], seg_menos_probable[1]) + 1,
                    [menos_probable, seg_menos_probable])
        
        fila_prioridad.append(nuevo_nodo)
        fila_prioridad.sort()
    
    # Consultar si se puede utilizar libreria heapq o así está bien

    return fila_prioridad[0] # Devolvemos el arbol sin la fila


def crear_diccionario(arbol):
    diccionario_codigos = {} 
    pila_busqueda = []  

    pila_busqueda.append(arbol + ("",))  
    
    while len(pila_busqueda) > 0:
        nodo_actual = pila_busqueda.pop()
        
        if type(nodo_actual[2]) == list:
            # El hijo izquierdo tiene "0" en el prefijo
            pila_busqueda.append(nodo_actual[2][1] + (nodo_actual[-1] + "0",))
            # El hijo derecho tiene "1" en el prefijo
            pila_busqueda.append(nodo_actual[2][0] + (nodo_actual[-1] + "1",))
            continue
        else:
            # El nodo es una hoja, así que obtenemos el código completo
            codigo = nodo_actual[-1]
            diccionario_codigos[nodo_actual[2]] = codigo
    
    return diccionario_codigos


def convertir_cadena(cadena_bits):
    bytes_lista = []
    longitud_original = len(cadena_bits)
    
    # Agrupa los bits en bytes
    for i in range(0, longitud_original, 8):
        sublista_bits = cadena_bits[i:i+8]  # Obtiene un grupo de 8 bits
        while len(sublista_bits) < 8:
            # Si el último grupo tiene menos de 8 bits, completa con ceros a la derecha
            sublista_bits.append(0)
        
        # Convierte la lista de bits a un entero
        byte_val = 0
        for bit in sublista_bits:
            byte_val = (byte_val << 1) | bit
            
        bytes_lista.append(byte_val)  # Añade el byte a la lista
    return bytes_lista

def comprimir(diccionario, contenido_binario, nombre_archivo):
    with open(nombre_archivo, 'wb') as archivo:
        vecaux = []
        for valor in contenido_binario:
            for b in diccionario[valor]:
                vecaux.extend([int(b)])
            
        longitud = len(vecaux)
        archivo.write(longitud.to_bytes(4, 'big')) # Se almacena la longitud exacta de bits

        # Serializar el diccionario
        # Almacenar como: [número de entradas del diccionario] [simbolo | longitud código | código binario]
        archivo.write(len(diccionario).to_bytes(2, 'big'))  # Máximo de 65535 símbolos

        for simbolo, codigo_binario in diccionario.items():
            longitud_codigo = len(codigo_binario)
            # Escribir símbolo (asumimos que es un byte)
            archivo.write(simbolo.to_bytes(1, 'big'))
            # Escribir longitud del código
            archivo.write(longitud_codigo.to_bytes(1, 'big'))
            # Escribir el código binario como entero
            archivo.write(int(codigo_binario, 2).to_bytes((longitud_codigo + 7) // 8, 'big'))
        archivo.write(bytearray(convertir_cadena(vecaux)))
    

def interpretar_bits(vector_bits, diccionario):

    diccionario_invertido = {v: k for k, v in diccionario.items()}
    secuencia_ascii = ""  # Cadena para almacenar la secuencia de caracteres ASCII resultante.
    temp_bits = ""  # Cadena temporal para acumular los bits.

    # Itera sobre cada bit en el vector de bits.
    for bit in vector_bits:
        temp_bits += bit  # Agrega el bit actual a la cadena temporal.
        
        # Comprueba si la cadena temporal coincide con alguna clave en el diccionario.
        if temp_bits in diccionario_invertido:
            simbolo = diccionario_invertido[temp_bits]  # Verifica si el valor del diccionario coincide con la cadena temporal.
            secuencia_ascii += chr(simbolo) # Convierte la clave (número) a su carácter ASCII.
            temp_bits = ""  # Reinicia la cadena temporal.

    return secuencia_ascii

def descomprimir(nombre_archivo_comprimido, nombre_archivo_descomprimido):
    with open(nombre_archivo_comprimido, 'rb') as archivo:
        #se leen los primeros 4 bytes para indetificar la longitud de la cadena original de bits a descomprimir
        longitud_original = int.from_bytes(archivo.read(4), 'big')
        #se recupera el diccionario
        diccionario = pickle.load(archivo)
        contenido_descomprimido = archivo.read()
        # Se convierte cada byte del contenido leído en una representación binaria de 8 bits
        bits = ''.join(f'{byte:08b}' for byte in contenido_descomprimido)
        #se acorta la cadena a su longitud original
        bits_originales = bits[:longitud_original]

    with open(nombre_archivo_descomprimido, 'wb') as archivo:
        aux = interpretar_bits(bits_originales, diccionario)
        archivo.write(aux.encode('utf-8'))

def calcular_tasa_compresion(archivo_original, archivo_comprimido):
    # Obtener el tamaño de los archivos en bytes
    tamaño_original = os.path.getsize(archivo_original)
    tamaño_comprimido = os.path.getsize(archivo_comprimido)

    # Calcular la tasa de compresión (TC)
    tasa_compresion = tamaño_original / tamaño_comprimido

    # Mostrar resultados
    print(f"d)Tasa de compresión: {tasa_compresion:.2f}:1")

def calcular_metricas(probabilidades, codigos):
    # Entropía
    entropia = 0
    for prob in probabilidades.values():
        entropia += prob * math.log2(1/prob)

    # Longitud media del código
    longitud_media = 0
    for simbolo in probabilidades:
        longitud_media += probabilidades[simbolo] * len(codigos[simbolo])

    # Rendimiento
    rendimiento = entropia / longitud_media if longitud_media > 0 else 0

    # Redundancia
    redundancia = 1 - rendimiento

    print(f"Rendimiento: {rendimiento:.4f} bits por símbolo")
    print(f"Redundancia: {redundancia:.4f}")
    return 0

def imprimir_tabla_frecuencias(probabilidades, diccionario):
    print("\nTabla de frecuencias:")
    print("Símbolo\tFrecuencia\tCódigo")
    for simbolo, probabilidad in probabilidades.items():
        # Convertimos el símbolo a su representación de carácter (o byte)
        simbolo_repr = simbolo if isinstance(simbolo, int) else chr(simbolo)
        codigo = diccionario[simbolo]
        print(f"{simbolo_repr}\t{probabilidad:.4f}\t\t{codigo}")
    print("\n")

if len(sys.argv) != 4:
    print("Uso: tpi3 {-c|-d} original compressed")
    sys.exit(1)

flag = sys.argv[1]
original = sys.argv[2]
compressed = sys.argv[3]

inicio = time.time()  # inicio del tiempo

if flag == '-c':
    contenido_binario = abrir_archivo(original)
    probabilidades = obtener_probabilidades(contenido_binario)
    arbol_Huffman = obtener_arbol_Huffman(probabilidades)
    diccionario = crear_diccionario(arbol_Huffman)
    comprimir(diccionario, contenido_binario, compressed)
    fin = time.time()  # final de tiempo
    print(f"c) La acción solicitada demoró: {fin - inicio:.4f} segundos")
    calcular_tasa_compresion(original, compressed)
    calcular_metricas(probabilidades, diccionario)
    # Activar esta función para ver la tabla de frecuencia de cada símbolo con su código
    imprimir_tabla_frecuencias(probabilidades, diccionario) 

elif flag == '-d':
    descomprimir(compressed, original)
    fin = time.time()  # final de tiempo
    print(f"Tiempo de descompresión solicitada: {fin - inicio:.4f} segundos")

else:
    print("FLAG INCORRECTA")