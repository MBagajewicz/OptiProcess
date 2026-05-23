# Planificación para la creación del Creador de Aplicaciones de Optimización

## Objetivo

Definir una sistema que permita capturar los distintos modelos ya desarrolados, tomando como ejemplo el caso STHE, y que sea capaz de consumir la información en el directorio correspondiente para construir una aplicación web de optimización en forma automática, la cual cargará los parametros de diseño en un archivo con la estructura de los ejemplos que se encuentran en Examples_STHE.py, llamará a Main.py y buscará los resultados que se devuelven en el archivo results_STHE_Example... correspondiente.

## Datos de partida

En el directorio **ejemplos-intefaz-grafica-html-estatica** se encuentran versiones base de las ventanas que constituyen el sistema que se tomará como modelo de lo que se debe construir automáticamente.
Las ventanas que se deben crear automáticamente son las correspondientes a los archivos: geometric-options-v1.html, login.html, main-menu.html, problem-data-v3.html, results-v2.html

La información desde la que se parte para dicho proceso de construcción se encuentra en el directorio **STHE**.


## Opciones de implementación

 * Opción 1: Partir de un archivo similar a los ejemplos en Examples_STHE.py, donde los comentarios puedan indicar etiquetas importantes, y que mediante un parser se creen los archivos HTML correspondientes a la interfaz grafica para ingresar los datos requeridos luego para crear la instancia a ejecutar con Main.py (un archivo con el formato de un ejemplo en el archivo Examples_STHE.py). 
 * Opción 2: Partir de un archivo estructurado tipo YAML, donde se definan los parametros cosntructivos y de diseño y las demás opciones para construir las paginas que conforman la intefaz web y luego se construya la interfaz grafica a partir de los datos que de importen del directorio. El archivo YAML podria tener un estructura similar a los ejemplos de Example_STHE.py
