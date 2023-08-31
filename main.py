import os
import xml.etree.ElementTree as ET
import subprocess
import graphviz

from listaSimple import ListaEnlazada

lista_senales = ListaEnlazada()
datos_cargados_y_procesados = False


def estudiante():
    print(
        """\n..................................................................\n
        
        Edgar Rolando Ramirez Lopez
        201212891
        Introduccion a la Programacion y Computacion 2
        Ingenieria en Ciencias y Sistemas
        4to Semestre
\n...................................................................\n"""
    )


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

        if nombre in nombres_senales:
            print(f"Señal con nombre duplicado encontrada: {nombre}. Se ignorará.")
            continue

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
    print("Calculando la matriz binaria...")
    matrices_finales_por_senal = []

    actual = lista_senales.cabeza
    while actual:
        nombre = actual.nombre
        tiempo = int(actual.tiempo)
        valor = int(actual.valor)
        amplitud = int(actual.amplitud)

        # Buscar la señal en la lista de señales procesadas
        senal_existente = next(
            (
                senal
                for senal in matrices_finales_por_senal
                if senal["nombre"] == nombre
            ),
            None,
        )

        if senal_existente:
            if amplitud > senal_existente["amplitud"]:
                senal_existente["amplitud"] = amplitud
                for fila in senal_existente["matriz_original"]:
                    fila.extend([0] * (amplitud - len(fila)))

            if tiempo > len(senal_existente["matriz_original"]):
                senal_existente["matriz_original"].extend(
                    [
                        [0] * senal_existente["amplitud"]
                        for _ in range(tiempo - len(senal_existente["matriz_original"]))
                    ]
                )

            senal_existente["grupos"].setdefault(tiempo, [])
            senal_existente["grupos"][tiempo].append((amplitud, valor))
            senal_existente["matriz_original"][tiempo - 1][amplitud - 1] = valor
        else:
            matriz_original = [[0] * amplitud for _ in range(tiempo)]
            matriz_original[tiempo - 1][amplitud - 1] = valor

            matrices_finales_por_senal.append(
                {
                    "nombre": nombre,
                    "amplitud": amplitud,
                    "matriz_original": matriz_original,
                    "grupos": {tiempo: [(amplitud, valor)]},
                }
            )

        actual = actual.siguiente

    print("Realizando suma de tuplas...")
    for senal in matrices_finales_por_senal:
        matriz_original = senal["matriz_original"]
        grupos_dict = {}

        for tiempo, grupo_data in senal["grupos"].items():
            tupla_binaria = tuple(
                1 if v > 0 else 0 for v in matriz_original[tiempo - 1]
            )
            if tupla_binaria not in grupos_dict:
                grupos_dict[tupla_binaria] = []
            grupos_dict[tupla_binaria].append(tiempo)

        matriz_final = []

        for tupla_binaria, tiempo_grupo in grupos_dict.items():
            new_row = [0] * senal["amplitud"]
            for tiempo in tiempo_grupo:
                for amplitud, valor in senal["grupos"][tiempo]:
                    new_row[amplitud - 1] += valor
            matriz_final.append(new_row)

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
                for amplitud_valor, valor in enumerate(
                    matriz_final[grupo_num - 1], start=1
                ):
                    file.write(
                        f'                <dato A="{amplitud_valor}">{valor}</dato>\n'
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
                datos_cargados_y_procesados = False
        elif option == 2:
            matrices_finales_por_senal = procesarxml()
            datos_cargados_y_procesados = True
        elif option == 3:
            escribir_xml_final(matrices_finales_por_senal)
        elif option == 4:
            estudiante()
        elif option == 5:
            if datos_cargados_y_procesados:
                lista_senales.mostrar_nombres()
                nombre_senal = input("Ingrese el nombre de la señal a mostrar: ")
                if lista_senales.buscar(nombre_senal):
                    lista_senales.mostrar_senal(nombre_senal)
                else:
                    print("La señal no existe.")
            else:
                print("No se han cargado ni procesado datos.")
        elif option == 0:
            break
        else:
            print("Opción incorrecta")
