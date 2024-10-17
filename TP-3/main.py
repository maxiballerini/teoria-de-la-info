import os
import heapq
from collections import Counter
import pickle

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
    secuencia_caracteres = ""
    temp_bits = "" 
    for bit in vector_bits:
        temp_bits += bit
        if temp_bits in diccionario:
            secuencia_caracteres += diccionario[temp_bits]
            temp_bits = ""
    
    return secuencia_caracteres

def comprimir(diccionario, contenido_binario,nombre_archivo):
    with open(nombre_archivo, 'wb') as archivo:
        vecaux = ""
        for valor in contenido_binario:
            vecaux += diccionario[valor]
        print(len(contenido_binario))
        print(len(vecaux))
        print(vecaux)
        #pickle.dump(diccionario, archivo)



def descomprimir(nombre_archivo_comprimido,nombre_archivo_descompimido):
    with open(nombre_archivo_comprimido, 'rb') as archivo:
        # Recupera el diccionario desde el archivo
        diccionario = pickle.load(archivo)
        contenido_descomprimido = archivo.read()

    with open(nombre_archivo_descompimido, 'w') as archivo:
        archivo.write(interpretar_bits(contenido_descomprimido,diccionario))


        

"""
def calcular_métricas(tamaño_original, tamaño_comprimido):
    tasa_compresion = tamaño_comprimido / tamaño_original
    rendimiento = math.log(tasa_compresion, 2)
    redundancia = 1 - rendimiento
    return tasa_compresion, rendimiento, redundancia
"""

# Obtener el directorio donde se encuentra el script
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Combinar la ruta de la carpeta con el nombre del archivo
#ruta_completa = os.path.join(directorio_actual, "prueba.txt")
ruta_completa = os.path.join(directorio_actual, "prueba.txt")
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

#archivo_comprimido = comprimir(diccionario, contenido_binario)
#tasa, rendimiento, redundancia = calcular_métricas(tamaño_original, tamaño_comprimido) #fala crear el tamorig y tamcompr

