# <p align="center">Teoría de la Información</p>
## Trabajo Práctico Integrador N° 2

La finalidad de este programa es actuar como una herramienta para realizar análisis en materia de la codificacion de la información.
A partir de un archivo de entrada que contiene palabras de código el programa efectúa cálculos específicos que facilitan el estudio y 
evaluación de distintos aspectos de la codificación, optimizando el proceso de análisis.

Las funcionalidades del programa son:

- Obtener el conjunto de palabras (separadas por espacios) contenidas en el archivo input.txt e identificar el alfabeto código
  que las compone.
- Verificar si la codificación cumple las inecuaciones de Kraft y McMillan y si se trata de un código instantáneo.
- Determinar si las palabras podrían conformar un código compacto y cuáles deberían ser sus probabilidades para que esto ocurra.
- En caso afirmativo, calcular la entropía de la fuente y la longitud media del código.
- Generar aleatoriamente un posible mensaje de N símbolos codificados emitido por dicha fuente y almacenarlo en el archivo output.txt.

Para ejecutar por consola el programa utilizar:

tpi2 input.txt [output.txt N]

Donde:

• tpi2 es el programa ejecutable  
• input.txt es un archivo de texto ASCII  
• output.txt es un archivo de texto ASCII (opcional)  
• N es un número natural (opcional)  
