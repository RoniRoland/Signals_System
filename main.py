def menuPrincipal():
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
    while True:
        try:
            option = int(input("Ingrese una opcion: "))
            return option
        except ValueError:
            print("Opcion incorrecta debe ser un numero")


if __name__ == "__main__":
    while True:
        option = menuPrincipal()
        try:
            if option == 1:
                break
            elif option == 2:
                break
            elif option == 3:
                break
            elif option == 4:
                break
            elif option == 5:
                break
            elif option == 0:
                break
            else:
                print("Opcion incorrecta")
        except ValueError:
            print("Opcion incorrecta")
    exit
