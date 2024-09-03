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

def crear_matriz_transicion(vector_archivo):
    """
    Crea una matriz de transición a partir de una secuencia de caracteres.
    
    Args:
        sec (str): La secuencia de caracteres.
    
    Returns:
        dict: Una matriz de transición representada como un diccionario de diccionarios.
        list: Lista de caracteres únicos en la secuencia.
    """
    # Obtener caracteres únicos
    caracteres = sorted(set(vector_archivo))
    num_caracteres = len(caracteres)
    
    # Crear una matriz de transición inicializada en 0
    matriz_transicion = {c1: {c2: 0 for c2 in caracteres} for c1 in caracteres}
    
    # Rellenar la matriz con las frecuencias de transición
    for i in range(len(vector_archivo) - 1):
        caracter_actual = vector_archivo[i]
        caracter_siguiente = vector_archivo[i + 1]
        matriz_transicion[caracter_siguiente][caracter_actual] += 1
    
    return matriz_transicion, caracteres

def imprimir_matriz(matriz_transicion, caracteres):
    """
    Imprime la matriz de transición en un formato legible.
    
    Args:
        matriz_transicion (dict): La matriz de transición.
        caracteres (list): Lista de caracteres únicos.
    """
    # Imprimir encabezado
    print(" ", " ".join(caracteres))
    
    # Imprimir filas
    for c1 in caracteres:
        fila = [str(matriz_transicion[c1].get(c2, 0)) for c2 in caracteres]
        print(c1, " ".join(fila))

def crea_vec_estacionario(frecuencias):
    vec = {}
    total = sum(frecuencias)
    vec = frecuencias
    vec = [elemento / total for elemento in vec]
    return vec

def contar_frecuencia(vector_arch,caracteres):
    # devuelve un vector con la frecuencia de las letras
    return [vector_arch.count(pos) for pos in caracteres]

# Ejemplo de uso
secuencia = "BBAAACCAAABCCCAACCCBBACCAABBAA"
matriz_transicion, caracteres = crear_matriz_transicion(secuencia)
print(contar_frecuencia(secuencia,caracteres))
print("\n\n")

print("Matriz de transición:")
imprimir_matriz(matriz_transicion, caracteres)