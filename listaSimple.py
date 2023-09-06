from nodo import Nodo
import subprocess
from os import startfile
import graphviz


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nombre, tiempo, amplitud, valor):
        nuevo_nodo = Nodo(nombre, tiempo, amplitud, valor)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def buscar(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.nombre == nombre:
                return True
            actual = actual.siguiente
        return False

    def delete_node(self, nombre, tiempo, amplitud):
        if self.cabeza is None:
            return
        if (
            self.cabeza.nombre == nombre
            and self.cabeza.tiempo == tiempo
            and self.cabeza.amplitud == amplitud
        ):
            self.cabeza = self.cabeza.siguiente
            return
        current = self.cabeza
        while current.siguiente:
            if (
                current.siguiente.nombre == nombre
                and current.siguiente.tiempo == tiempo
                and current.siguiente.amplitud == amplitud
            ):
                current.siguiente = current.siguiente.siguiente
                return
            current = current.siguiente

    def mostrar_nombres(self):
        nombres = set()
        actual = self.cabeza
        while actual:
            nombres.add(actual.nombre)
            actual = actual.siguiente
        print("\nSeñales disponibles:")
        for nombre in nombres:
            print(nombre)

    def mostrar_senal(self, nombre_senal):
        actual = self.cabeza
        while actual:
            if actual.nombre == nombre_senal:
                print("\nMatriz de la señal:", actual.nombre)
                while actual and actual.nombre == nombre_senal:
                    print(
                        "Tiempo:",
                        actual.tiempo,
                        "Amplitud:",
                        actual.amplitud,
                        "Valor:",
                        actual.valor,
                    )
                    actual = actual.siguiente
                return
            actual = actual.siguiente
        print("La señal no fue encontrada.")

    def writeNodes(self, f):
        aux = self.cabeza
        count = 1

        while aux is not None:
            f.write(f'node{count} [shape=oval, label=" {aux.valor} "]\n')
            aux = aux.siguiente
            count += 1

        aux = self.cabeza
        i = 1
        while aux.siguiente is not None:
            f.write(f"node{i} -> node{i + 1}\n")
            aux = aux.siguiente
            i += 1

    def generateGraphvizCode(self, nombre_senal):
        fullNameTxt = f"{nombre_senal}.dot"
        fullNameImg = f"{nombre_senal}.jpg"

        try:
            f = open(fullNameTxt, "w")
            f.write("digraph G {\n")
            f.write("rankdir=TB;\n")
            f.write(f'nodeRoot [shape=circle, label=" {nombre_senal} "]\n')
            f.write('nodeTiempo [shape=circle, label=" t=n  "]\n')
            f.write('nodeAmplitud [shape=circle, label=" a=n  "]\n')
            f.write("nodeRoot -> nodeTiempo\n")
            f.write("nodeRoot -> nodeAmplitud\n")
            f.write(
                "nodeRoot -> node1\n"
            )  # Cambia node1 por el número correcto de inicio
            self.writeNodes(f)
            f.write("}")
            f.close()

            command = ["dot", "-Tjpg", fullNameTxt, "-o", fullNameImg]
            subprocess.call(command)

            startfile(fullNameImg)
        except:
            print("Error al generar el gráfico.")
            f.close()
