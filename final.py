import datetime

# Información del equipo/desarrollador
INFO = """
Sistema de Gestión de Tareas
Nombres: Santiago Duran / Artemisa Tsubaki
Estructuras de Datos y Algoritmos I

"""

# Clase para representar cada tarea en una lista enlazada
class Tarea:
    def __init__(self, id, descripcion, fecha_venc, prioridad):
        self.id = id
        self.descripcion = descripcion
        self.fecha_venc = fecha_venc
        self.prioridad = prioridad
        self.sig = None

# Clase para la lista enlazada de tareas
class ListaTareas:
    def __init__(self):
        self.inicio = None

    def agregar_tarea(self, tarea):
        if self.inicio is None:
            self.inicio = tarea
        else:
            actual = self.inicio
            while actual.sig:
                actual = actual.sig
            actual.sig = tarea

    def buscar_tarea(self, id):
        actual = self.inicio
        while actual:
            if actual.id == id:
                return actual
            actual = actual.sig
        return None

    def eliminar_tarea(self, id):
        actual = self.inicio
        anterior = None
        while actual:
            if actual.id == id:
                if anterior:
                    anterior.sig = actual.sig
                else:
                    self.inicio = actual.sig
                return actual
            anterior = actual
            actual = actual.sig
        return None

    def mostrar_tareas(self):
        actual = self.inicio
        if not actual:
            print("No hay tareas registradas.")
        while actual:
            print(f"ID: {actual.id} | Desc: {actual.descripcion} | Vence: {actual.fecha_venc} | Prioridad: {actual.prioridad}")
            actual = actual.sig

# Clase para la pila (historial de acciones)
class PilaDeshacer:
    def __init__(self):
        self.pila = []

    def registrar(self, accion, tarea):
        self.pila.append((accion, tarea))

    def deshacer(self, lista_tareas):
        if not self.pila:
            print("No hay acciones para deshacer.")
            return
        accion, tarea = self.pila.pop()
        if accion == "agregar":
            lista_tareas.eliminar_tarea(tarea.id)
            print(f"Deshecho: Se eliminó tarea {tarea.id}")
        elif accion == "eliminar":
            lista_tareas.agregar_tarea(tarea)
            print(f"Deshecho: Se restauró tarea {tarea.id}")
        elif accion == "modificar":
            original = lista_tareas.buscar_tarea(tarea.id)
            if original:
                original.descripcion = tarea.descripcion
                original.fecha_venc = tarea.fecha_venc
                original.prioridad = tarea.prioridad
                print(f"Deshecho: Se restauraron los valores originales de la tarea {tarea.id}")

# Clase para la cola de impresión
class ColaImpresion:
    def __init__(self):
        self.cola = []

    def agregar_a_cola(self, tarea):
        self.cola.append(tarea)

    def imprimir_tareas(self):
        if not self.cola:
            print("La cola de impresión está vacía.")
        while self.cola:
            tarea = self.cola.pop(0)
            print(f"[IMPRESO] ID: {tarea.id} - {tarea.descripcion} - Vence: {tarea.fecha_venc} - Prioridad: {tarea.prioridad}")

# Función principal con menú de consola
def menu():
    tareas = ListaTareas()
    historial = PilaDeshacer()
    impresora = ColaImpresion()
    id_actual = 1

    while True:
        print(INFO)
        print("\nMenú Principal:")
        print("1. Añadir Tarea")
        print("2. Modificar Tarea")
        print("3. Eliminar Tarea")
        print("4. Ver Tareas")
        print("5. Deshacer Última Acción")
        print("6. Añadir a Cola de Impresión")
        print("7. Imprimir Tareas")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            desc = input("Descripción: ")
            fecha = input("Fecha de vencimiento (YYYY-MM-DD): ")
            prioridad = input("Prioridad (Alta/Media/Baja): ")
            nueva = Tarea(id_actual, desc, fecha, prioridad)
            tareas.agregar_tarea(nueva)
            historial.registrar("agregar", nueva)
            print(f"Tarea {id_actual} añadida.")
            id_actual += 1

        elif opcion == "2":
            id_mod = int(input("ID de la tarea a modificar: "))
            tarea = tareas.buscar_tarea(id_mod)
            if tarea:
                copia = Tarea(tarea.id, tarea.descripcion, tarea.fecha_venc, tarea.prioridad)
                tarea.descripcion = input("Nueva descripción: ")
                tarea.fecha_venc = input("Nueva fecha (YYYY-MM-DD): ")
                tarea.prioridad = input("Nueva prioridad: ")
                historial.registrar("modificar", copia)
                print("Tarea modificada.")
            else:
                print("Tarea no encontrada.")

        elif opcion == "3":
            id_elim = int(input("ID de la tarea a eliminar: "))
            tarea = tareas.eliminar_tarea(id_elim)
            if tarea:
                historial.registrar("eliminar", tarea)
                print("Tarea eliminada.")
            else:
                print("Tarea no encontrada.")

        elif opcion == "4":
            tareas.mostrar_tareas()

        elif opcion == "5":
            historial.deshacer(tareas)

        elif opcion == "6":
            id_imp = int(input("ID de la tarea a imprimir: "))
            tarea = tareas.buscar_tarea(id_imp)
            if tarea:
                impresora.agregar_a_cola(tarea)
                print("Tarea añadida a la cola de impresión.")
            else:
                print("Tarea no encontrada.")

        elif opcion == "7":
            impresora.imprimir_tareas()

        elif opcion == "8":
            print("Saliendo del programa. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()
