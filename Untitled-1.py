def crear_matriz_transicion(sec):
    """
    Crea una matriz de transición a partir de una secuencia de caracteres.
    
    Args:
        sec (str): La secuencia de caracteres.
    
    Returns:
        dict: Una matriz de transición representada como un diccionario de diccionarios.
        list: Lista de caracteres únicos en la secuencia.
    """
    # Obtener caracteres únicos
    caracteres = sorted(set(sec))
    num_caracteres = len(caracteres)
    
    # Crear una matriz de transición inicializada en 0
    matriz_transicion = {c1: {c2: 0 for c2 in caracteres} for c1 in caracteres}
    
    # Rellenar la matriz con las frecuencias de transición
    for i in range(len(sec) - 1):
        caracter_actual = sec[i]
        caracter_siguiente = sec[i + 1]
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

# Ejemplo de uso
secuencia = "BBAAACCAAABCCCAACCCBBACCAABBAA"
matriz_transicion, caracteres = crear_matriz_transicion(secuencia)

print("Matriz de transición:")
imprimir_matriz(matriz_transicion, caracteres)