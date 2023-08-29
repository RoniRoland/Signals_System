import os
import xml.etree.ElementTree as ET
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
        print("Nombre de la señal:", nombre)
        nombres_senales.add(nombre)

        for dato in senal.findall("dato"):
            tiempo = dato.get("t")
            amplitud = dato.get("A")
            valor = int(dato.text)
            print("Tiempo:", tiempo, "Amplitud:", amplitud, "Valor interno:", valor)
            lista_senales.agregar(nombre, tiempo, amplitud, valor)

    print("\nSeñales disponibles:")
    for nombre_senal in nombres_senales:
        print("Nombre de la señal:", nombre_senal)


def procesarxml():
    if not lista_senales.cabeza:
        print("No hay datos cargados. Cargue un archivo primero.")
        return

    # Crear diccionario para almacenar los valores originales por señal
    valores_originales_por_senal = {}

    # Llenar el diccionario con los valores originales por señal
    actual = lista_senales.cabeza
    while actual:
        nombre = actual.nombre
        tiempo = int(actual.tiempo)
        valor = int(actual.valor)
        amplitud = int(actual.amplitud)

        if nombre not in valores_originales_por_senal:
            valores_originales_por_senal[nombre] = [[0] * 4 for _ in range(5)]

        valores_originales_por_senal[nombre][tiempo - 1][amplitud - 1] = valor

        actual = actual.siguiente

    # Crear matrices binarias por señal y calcular las matrices finales agrupadas
    for nombre, matriz_original in valores_originales_por_senal.items():
        matriz_binaria = [
            [1 if val > 0 else 0 for val in fila] for fila in matriz_original
        ]
        grupos = {}

        for tiempo, fila_binaria in enumerate(matriz_binaria):
            tupla_binaria = tuple(fila_binaria)
            if tupla_binaria not in grupos:
                grupos[tupla_binaria] = []
            grupos[tupla_binaria].append(tiempo + 1)

        matriz_final = [[0] * 4 for _ in range(len(grupos))]
        for index, tiempo_grupo in enumerate(grupos.values()):
            for tiempo in tiempo_grupo:
                for i in range(4):
                    matriz_final[index][i] += matriz_original[tiempo - 1][i]

        # Mostrar las matrices binarias por señal
        print("\nMatriz binaria", nombre)
        print("\t", "  ".join("Ampl" + str(i + 1) for i in range(4)))
        for tiempo, fila_binaria in enumerate(matriz_binaria):
            print(
                "T" + str(tiempo + 1), "\t", "  ".join(str(val) for val in fila_binaria)
            )

        # Mostrar la matriz final agrupada por señal
        print("\nMatriz final agrupada", nombre)
        print("\t", "  ".join("Ampl" + str(i + 1) for i in range(4)))
        for tiempo_grupo, fila_final in zip(grupos.values(), matriz_final):
            print(
                "T" + "".join(str(tiempo) for tiempo in tiempo_grupo),
                "\t",
                "  ".join(str(val) for val in fila_final),
            )


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
            procesarxml()
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
