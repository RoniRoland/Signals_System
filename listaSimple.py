from nodo import Nodo


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

    def mostrar_nombres(self):
        nombres = set()
        actual = self.cabeza
        while actual:
            nombres.add(actual.nombre)
            actual = actual.siguiente
        for nombre in nombres:
            print("Nombre de la señal:", nombre)

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
