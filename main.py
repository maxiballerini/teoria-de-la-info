def cargar_caracteres_en_vector(nombre_archivo):
    # Inicializar una lista para almacenar los caracteres
    vector_caracteres = []
    # Abrir el archivo en modo lectura
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        # Leer el contenido del archivo
        contenido = archivo.read()  
        # Agregar cada carácter del contenido a la lista
        vector_caracteres.extend(contenido)
    return vector_caracteres


def contar_frecuencias(vector):
    """
    Genera dos vectores: uno con los caracteres únicos y otro con sus frecuencias.
    Luego ordena los caracteres por frecuencia en orden descendente.
    
    Args:
        vector (list): Lista de caracteres.
    
    Returns:
        tuple: Dos listas, la primera con los caracteres únicos y la segunda con las frecuencias.
    """
    # Crear un diccionario para contar frecuencias
    frecuencias = {}
    
    # Contar la frecuencia de cada carácter
    for caracter in vector:
        if caracter in frecuencias:
            frecuencias[caracter] += 1
        else:
            frecuencias[caracter] = 1
    
    # Ordenar los caracteres por frecuencia en orden descendente
    tipos_ordenados = sorted(frecuencias.keys(), key=lambda k: frecuencias[k], reverse=True)
    frecuencias_ordenadas = [frecuencias[tipo] for tipo in tipos_ordenados]
    
    return tipos_ordenados, frecuencias_ordenadas

def crea_vec_estacionario(frecuencias):
    vec = {}
    total = sum(frecuencias)
    vec = frecuencias
    vec = [elemento / total for elemento in vec]
    return vec
    
def crea_matriz_trans(caracteres,):

    return
# Ejemplo de uso de la función
nombre_archivo = 'D:/universidad/teoriainfo/tp1/.venv/tp1/tp1_sample3.txt'
vec = cargar_caracteres_en_vector(nombre_archivo)
caracteres, frecuencias = contar_frecuencias(vec)
vec_estacionario = crea_vec_estacionario(frecuencias)
print(vec_estacionario)
print(caracteres)
print("Frecuencias:", frecuencias)
