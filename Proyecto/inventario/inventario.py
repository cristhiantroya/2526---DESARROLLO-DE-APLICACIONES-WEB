from inventario.productos import Producto

class Inventario:
    def __init__(self):
        # Diccionario con clave = ID del producto
        self.productos = {}

    def agregar_producto(self, producto: Producto):
        self.productos[producto.id] = producto

    def eliminar_producto(self, id):
        if id in self.productos:
            del self.productos[id]

    def actualizar_producto(self, id, cantidad=None, precio=None):
        if id in self.productos:
            if cantidad is not None:
                self.productos[id].cantidad = cantidad
            if precio is not None:
                self.productos[id].precio = precio

    def buscar_por_nombre(self, nombre):
        return [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]

    def mostrar_todos(self):
        return list(self.productos.values())
