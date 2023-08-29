import os
import xml.etree.ElementTree as ET
import subprocess

from listaSimple import ListaEnlazada

lista_senales = ListaEnlazada()


def elegirArchivo():
    while True:
        nombreArchivo = input("Escribe el nombre o ruta del archivo para cargar: ")
        if nombreArchivo.endswith(".xml"):
            if os.path.exists(nombreArchivo):
                print("\n*-*-*-*-*-Archivo cargado exitosamente.*-*-*-*-*-\n")
                return nombreArchivo
            else:
                print("El archivo no existe.")
                return None
        else:
            print("El archivo debe tener la extensión .xml.")


def cargar_datos_desde_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    nombres_senales = set()

    for senal in root.findall("senal"):
        nombre = senal.get("nombre")
        # print("Nombre de la señal:", nombre)
        nombres_senales.add(nombre)

        for dato in senal.findall("dato"):
            tiempo = dato.get("t")
            amplitud = dato.get("A")
            valor = int(dato.text)
            # print("Tiempo:", tiempo, "Amplitud:", amplitud, "Valor interno:", valor)
            lista_senales.agregar(nombre, tiempo, amplitud, valor)

    # print("\nSeñales disponibles:")
    # for nombre_senal in nombres_senales:
    # print("Nombre de la señal:", nombre_senal)


if __name__ == "__main__":
    while True:
        print(
            """\n==================================================================
        Proyecto 1 - Introduccion a la Programacion y Computacion 2
==================================================================
        # Sistema de Señales de Audio:\n
        
        1.- Cargar Archivo
        2.- Procesar Archivo
        3.- Escribir archivo salida
        4.- Mostrar datos del estudiante
        5.- Generar Grafica
        0.- Salir
\n...................................................................\n"""
        )

        option = input("Ingrese una opción: ")
        try:
            option = int(option)
        except ValueError:
            print("Opción incorrecta. Debe ser un número del rango 0 a 2")
            continue

        if option == 1:
            archivo = elegirArchivo()
            if archivo is not None:
                cargar_datos_desde_xml(archivo)
        elif option == 2:
            break
        elif option == 3:
            break
        elif option == 4:
            break
        elif option == 5:
            print("\nSeñales disponibles:")
            lista_senales.mostrar_nombres()
            nombre_senal = input("Ingrese el nombre de la señal a mostrar: ")
            if lista_senales.buscar(nombre_senal):
                lista_senales.mostrar_senal(nombre_senal)
            else:
                print("La señal no existe.")
        elif option == 0:
            break
        elif option == 0:
            break
        else:
            print("Opción incorrecta")
