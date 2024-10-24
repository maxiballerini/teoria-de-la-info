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
    #res = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
    return res

def obtener_arbol_Huffman(probabilidades):
    fila_prioridad = []

    for simbolo,probabilidad in probabilidades.items():
        heapq.heappush(fila_prioridad, (probabilidad, 0, simbolo)) 

    while len(fila_prioridad) > 1:
        menos_probable = heapq.heappop(fila_prioridad) 
        seg_menos_probable = heapq.heappop(fila_prioridad) 
        # Este nuevo nodo tiene probabilidad e1[0]+e2[0]
        # y profundidad mayor al nuevo nodo
        nuevo_nodo = (menos_probable[0]+seg_menos_probable[0],max(menos_probable[1],seg_menos_probable[1])+1,[menos_probable,seg_menos_probable])
        heapq.heappush(fila_prioridad,nuevo_nodo)
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

def convertir_cadena(cadena_bits):
    bytes_lista = []
    longitud_original = len(cadena_bits)
    
    # Agrupa los bits en bytes
    for i in range(0, longitud_original, 8):
        byte_str = cadena_bits[i:i+8]  # Obtiene un grupo de 8 bits
        if len(byte_str) < 8:
            # Si el último grupo tiene menos de 8 bits, completa con ceros a la derecha
            byte_str = byte_str.ljust(8, '0')
        
        # Convierte la cadena de bits a un entero
        byte_val = int(byte_str, 2)  # Convierte de binario a entero
        bytes_lista.append(byte_val)  # Añade el byte a la lista
    return bytes_lista

def comprimir(diccionario, contenido_binario,nombre_archivo):
    with open(nombre_archivo, 'wb') as archivo:
        vecaux = ""
        for valor in contenido_binario:
            vecaux += diccionario[valor]
            
        longitud = len(vecaux)
        #se guarda un int (4 bytes) que indica la longitud de la cadena comprimida para luego recortarla ya que
        #podria pasar que cuando se convierte la cadena de bits a bytes esta se auntocomplete en el ultimo byte con 0
        archivo.write(longitud.to_bytes(4, 'big'))
        #se usa la libreria pickle donde "pickle.dump" es una fucnion encargada de alamcenar un diccionario en un archivo
        pickle.dump(diccionario, archivo)
        archivo.write(bytearray(convertir_cadena(vecaux)))
    


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

def calcular_metricas(archivo_original, archivo_comprimido):
    # Obtener el tamaño de los archivos en bytes
    tamaño_original = os.path.getsize(archivo_original)
    tamaño_comprimido = os.path.getsize(archivo_comprimido)

    # Calcular la tasa de compresión (TC)
    tasa_compresion = tamaño_comprimido / tamaño_original

    # Contar el número de símbolos en el archivo original
    with open(archivo_original, 'rb') as f:
        contenido = f.read()
        n = len(contenido)  # Número de símbolos (caracteres)

    # Calcular el rendimiento (R)
    rendimiento = (tamaño_comprimido * 8) / n  # En bits por símbolo

    # Calcular la redundancia
    k = len(set(contenido)) 
    log_k = math.log2(k)
    redundancia = 1 - (rendimiento / log_k)

    # Mostrar resultados
    print(f"D)Tasa de compresión: {tasa_compresion:.4f}")
    print(f"Rendimiento: {rendimiento:.4f} bits por símbolo")
    print(f"Redundancia: {redundancia:.4f}")

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
    print(f"\nTiempo de compresión solicitada: {fin - inicio:.4f} segundos")
    calcular_metricas(original, compressed)
    # Activar esta función para ver la tabla de frecuencia de cada símbolo con su código
    #imprimir_tabla_frecuencias(probabilidades, diccionario) 

elif flag == '-d':
    descomprimir(compressed, original)
    fin = time.time()  # final de tiempo
    print(f"\nTiempo de descompresión solicitada: {fin - inicio:.4f} segundos")

else:
    print("FLAG INCORRECTA")