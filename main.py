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


def procesarxml():
    if not lista_senales.cabeza:
        print("No hay datos cargados. Cargue un archivo primero.")
        return []

    matrices_finales_por_senal = []

    actual = lista_senales.cabeza
    while actual:
        nombre = actual.nombre
        tiempo = int(actual.tiempo)
        valor = int(actual.valor)
        amplitud = int(actual.amplitud)

        if (
            not matrices_finales_por_senal
            or matrices_finales_por_senal[-1]["nombre"] != nombre
        ):
            matrices_finales_por_senal.append(
                {
                    "nombre": nombre,
                    "amplitud": amplitud,
                    "matriz_original": [[0] * 4 for _ in range(5)],
                    "grupos": {},
                }
            )

        matrices_finales_por_senal[-1]["grupos"].setdefault(tiempo, [])
        matrices_finales_por_senal[-1]["grupos"][tiempo].append((amplitud, valor))
        matrices_finales_por_senal[-1]["matriz_original"][tiempo - 1][
            amplitud - 1
        ] = valor

        actual = actual.siguiente

    for senal in matrices_finales_por_senal:
        matriz_original = senal["matriz_original"]
        matriz_binaria = [
            [1 if val > 0 else 0 for val in fila] for fila in matriz_original
        ]
        grupos_dict = {}

        for tiempo, grupo_data in senal["grupos"].items():
            tupla_binaria = tuple(
                1 if v > 0 else 0 for v in matriz_original[tiempo - 1]
            )
            if tupla_binaria not in grupos_dict:
                grupos_dict[tupla_binaria] = []
            grupos_dict[tupla_binaria].append(tiempo)

        matriz_final = [[0] * 4 for _ in range(len(grupos_dict))]
        for index, tiempo_grupo in enumerate(grupos_dict.values()):
            for tiempo in tiempo_grupo:
                for amplitud, valor in senal["grupos"][tiempo]:
                    matriz_final[index][amplitud - 1] += valor

        senal["matriz_final"] = matriz_final
        senal["grupos"] = grupos_dict

    print("Procesado completado.")
    return matrices_finales_por_senal


def escribir_xml_final(matrices_finales_por_senal):
    if not matrices_finales_por_senal:
        print("No hay datos procesados. Procesa los datos primero en la opción 2.")
        return

    nombre_archivo_salida = input(
        "Ingrese el nombre del archivo XML de salida (sin extensión .xml): "
    )
    archivo_salida = nombre_archivo_salida + ".xml"

    with open(archivo_salida, "w", encoding="utf-8") as file:
        file.write('<?xml version="1.0" encoding="utf-8"?>\n')
        file.write("<senalesReducidas>\n")

        for senal in matrices_finales_por_senal:
            nombre_senal = senal["nombre"]
            matriz_final = senal["matriz_final"]
            amplitud_senal = senal["amplitud"]

            file.write(f'    <senal nombre="{nombre_senal}" A="{amplitud_senal}">\n')

            for grupo_num, (tupla_binaria, tiempo_grupo) in enumerate(
                senal["grupos"].items(), start=1
            ):
                tiempos = ",".join(str(tiempo) for tiempo in tiempo_grupo)
                file.write(f'        <grupo g="{grupo_num}">\n')
                file.write(f"            <tiempos>{tiempos}</tiempos>\n")
                file.write(f"            <datosGrupo>\n")
                for amplitud_valor in matriz_final[grupo_num - 1]:
                    file.write(
                        f'                <dato A="{amplitud_valor + 1}">{amplitud_valor}</dato>\n'
                    )
                file.write(f"            </datosGrupo>\n")
                file.write(f"        </grupo>\n")

            file.write(f"    </senal>\n")

        file.write("</senalesReducidas>\n")

    print(f"Archivo {archivo_salida} creado exitosamente.")
    subprocess.call(["start", archivo_salida], shell=True)


if __name__ == "__main__":
    matrices_finales_por_senal = []
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
            matrices_finales_por_senal = procesarxml()
        elif option == 3:
            escribir_xml_final(matrices_finales_por_senal)
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
