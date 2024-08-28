
def contar_frecuencias(nombre_archivo):
    # Crear un diccionario para contar la frecuencia de cada carácter
    frecuencias = {}
    caracteres = {}

    try:
        # Abrir el archivo en modo lectura
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            # Leer el contenido del archivo
            contenido = archivo.read()
            
            # Iterar sobre cada carácter en el contenido
            for caracter in contenido:
                # Actualizar la frecuencia del carácter en el diccionario
                if caracter in frecuencias:
                    frecuencias[caracter] += 1
                else:
                    caracteres[caracter] = caracter
                    frecuencias[caracter] = 1
        
        # Crear una lista de frecuencias
        lista_frecuencias = [frecuencias[caracter] for caracter in frecuencias]
        lista_caracteres= [caracteres[caracter] for caracter in caracteres]
        return lista_frecuencias , lista_caracteres

    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encontró.")
        return []
    except IOError as e:
        print(f"Error de entrada/salida: {e}")
        return []

def vec_extension():
    

# Ejemplo de uso de la función
nombre_archivo = 'D:/universidad/teoriainfo/tp1/.venv/tp1/tp1_sample3.txt'
frecuencias, caracteres = contar_frecuencias(nombre_archivo)
print(caracteres)
print("Frecuencias:", frecuencias)
