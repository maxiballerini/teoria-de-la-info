import os
import heapq
from collections import Counter

def abrir_archivo(nombre_archivo):
    # Abriendo un archivo de imagen en modo binario
    with open(nombre_archivo, "rb") as archivo:
        contenido_binario = archivo.read()  # Lee todo el contenido del archivo como bytes

    #print(contenido_binario)  # Imprime los bytes, puedes procesarlos o guardarlos en un arreglo

    #Contar la frecuencia de cada byte
    conteo_bytes = Counter(contenido_binario)

    #Separar los bytes únicos y sus frecuencias en dos listas
    bytes_unicos = list(conteo_bytes.keys())
    frecuencia_bytes = list(conteo_bytes.values())

    #print("Bytes únicos:", bytes_unicos)
    #print("Frecuencia de bytes:", frecuencia_bytes)
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


def comprimir(diccionario, contenido):
    resultado = ""
    for simbolo in contenido:
        codigo = diccionario[simbolo]
        resultado = resultado + codigo
    # Agregamos el '1' al inicio para no perder los '0' que puede llegar a haber en la izquierda
    resultado = '1' + resultado + diccionario['fin']
    resultado = resultado + (len(resultado) % 8 * "0")
    return int(resultado, 2) 

def calcular_métricas(tamaño_original, tamaño_comprimido):
    tasa_compresion = tamaño_comprimido / tamaño_original
    rendimiento = math.log(tasa_compresion, 2)
    redundancia = 1 - rendimiento
    return tasa_compresion, rendimiento, redundancia


# Obtener el directorio donde se encuentra el script
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Combinar la ruta de la carpeta con el nombre del archivo
#ruta_completa = os.path.join(directorio_actual, "prueba.txt")
ruta_completa = os.path.join(directorio_actual, "facultad.png")
# Leemos el archivo de entrada y lo almacenamos
contenido_binario = abrir_archivo(ruta_completa)
# Calculamos la distribución de probabilidades para cada símbolo
probabilidades = obtener_probabilidades(contenido_binario)
print(probabilidades)

arbol_Huffman = obtener_arbol_Huffman(probabilidades)
diccionario = crear_diccionario(arbol_Huffman)
archivo_comprimido = comprimir(diccionario, contenido_binario)
tasa, rendimiento, redundancia = calcular_métricas(tamaño_original, tamaño_comprimido) #fala crear el tamorig y tamcompr


