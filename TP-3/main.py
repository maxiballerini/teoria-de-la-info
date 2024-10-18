import os
import heapq
from collections import Counter
import pickle
import sys
import time

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
    secuencia_ascii = ""  # Cadena para almacenar la secuencia de caracteres ASCII resultante.
    temp_bits = ""  # Cadena temporal para acumular los bits.

    # Itera sobre cada bit en el vector de bits.
    for bit in vector_bits:
        temp_bits += bit  # Agrega el bit actual a la cadena temporal.
        
        # Comprueba si la cadena temporal coincide con alguna clave en el diccionario.
        for clave, valor in diccionario.items():
            if temp_bits == valor:  # Verifica si el valor del diccionario coincide con la cadena temporal.
                secuencia_ascii += chr(clave)  # Convierte la clave (número) a su carácter ASCII.
                temp_bits = ""  # Reinicia la cadena temporal.

    return secuencia_ascii

def converir_cadena(cadena_bits):
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
        archivo.write(longitud.to_bytes(4, 'big'))
        pickle.dump(diccionario, archivo)
        archivo.write(bytearray(converir_cadena(vecaux)))
    


def descomprimir(nombre_archivo_comprimido,nombre_archivo_descompimido):
    with open(nombre_archivo_comprimido, 'rb') as archivo:
        longitud_original = int.from_bytes(archivo.read(4), 'big')
        diccionario = pickle.load(archivo)
        contenido_descomprimido = archivo.read()
        bits = ''.join(f'{byte:08b}' for byte in contenido_descomprimido)
        bits_originales = bits[:longitud_original]

    with open(nombre_archivo_descompimido, 'w') as archivo:
        aux =interpretar_bits(bits_originales,diccionario)
        archivo.write(aux)


        

"""
def calcular_métricas(tamaño_original, tamaño_comprimido):
    tasa_compresion = tamaño_comprimido / tamaño_original
    rendimiento = math.log(tasa_compresion, 2)
    redundancia = 1 - rendimiento
    return tasa_compresion, rendimiento, redundancia
"""



"""
if len(sys.argv) == 4:

    #ESTO HAY  QUE CAMBIARLO , RTA COMPLETA DEBERIA SER EL ARGUMENTO "ORIGINAL"

    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    # Combinar la ruta de la carpeta con el nombre del archivo
    #ruta_completa = os.path.join(directorio_actual, "prueba.txt")
    ruta_completa = os.path.join(directorio_actual, "prueba.txt")
    # Leemos el archivo de entrada y lo almacenamos
    contenido_binario = abrir_archivo(ruta_completa)



    flag = sys.argv[1]
    original = sys.argv[2]
    compressed = sys.argv[3]
    if flag == '-c':
        contenido_binario = abrir_archivo(ruta_completa)
        probabilidades = obtener_probabilidades(contenido_binario)
        arbol_Huffman = obtener_arbol_Huffman(probabilidades)
        diccionario = crear_diccionario(arbol_Huffman)
        #COMPRIMIDO.DAT deberia ser el argumento compressed
        comprimir(diccionario, contenido_binario,"comprimido.dat")
    elif flag == '-d':
        #lo mismo para los nombre de l0so archivos aca
        descomprimir("comprimido.dat","descomprimido.dat")
    else:
        print("FLAG INCORRECTA")
"""

inicio = time.time() # inicio del tiempo

# Obtener el directorio donde se encuentra el script
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Combinar la ruta de la carpeta con el nombre del archivo
ruta_completa = os.path.join(directorio_actual, "prueba.txt")
#ruta_completa = os.path.join(directorio_actual, "facultad.png")
# Leemos el archivo de entrada y lo almacenamos
contenido_binario = abrir_archivo(ruta_completa)
# Calculamos la distribución de probabilidades para cada símbolo
probabilidades = obtener_probabilidades(contenido_binario)
print("probabilidades: ",probabilidades,"\n")

arbol_Huffman = obtener_arbol_Huffman(probabilidades)
print("ARBOL:",arbol_Huffman,"\n")

diccionario = crear_diccionario(arbol_Huffman)
print("diccionario",diccionario,"\n")

comprimir(diccionario, contenido_binario,"comprimido.dat")
descomprimir("comprimido.dat","descomprimido.dat")

fin = time.time() # final de tiempo

print(f"\nC)Tiempo de la accion solicitada: {fin - inicio:.4f} segundos")

#tasa, rendimiento, redundancia = calcular_métricas(tamaño_original, tamaño_comprimido) #fala crear el tamorig y tamcompr
