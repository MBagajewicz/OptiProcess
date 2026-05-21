# Planificación para la creación del Creador de Aplicaciones de Optimización

## Objetivo

Definir una sistema que permita capturar los distintos modelos ya desarrolados, tomando como ejemplo el caso STHE, y que sea capaz de consumir la información en el directorio correspondiente para construir una aplicación web de optimización en forma automática, la cual cargará los parametros de diseño y llemará a Main.py

## Datos de partida

El el directorio **ejemplos-intefaz-grafica-html-estatica** se encuentran versiones base de las ventanas que constituyen el sistema que se tomará como modelo de lo que se debe construir automáticamente.

La información desde la que se parte pra dicho proceso de construcción se encuentra en el directorio **STHE**.


## Opciones de implementación

 * Opción 1: Partir de un archivo similar a los ejemplos, pero que se lea el contenido de mediante un parser.
 * Opción 2: Partir de un archivo estructurado tipo YAML, donde se definan los elementos de la pagina y luego se construya a partir de los datos que de importen del directorio (u objetos si se trabaja con clases).
