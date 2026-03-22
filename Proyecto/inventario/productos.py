from conexion.conexion import get_db_connection

class Producto:
    def __init__(self, id_producto, marca, modelo, precio, stock):
        self.id_producto = id_producto
        self.marca = marca
        self.modelo = modelo
        self.precio = precio
        self.stock = stock

    def __str__(self):
        return f"{self.id_producto} - {self.marca} {self.modelo} | Stock: {self.stock} | Precio: {self.precio}"


def listar_productos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_producto, marca, modelo, precio, stock FROM productos")
    filas = cursor.fetchall()
    conn.close()
    return [Producto(*fila) for fila in filas]

def insertar_producto(marca, modelo, precio, stock):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (marca, modelo, precio, stock) VALUES (%s, %s, %s, %s)",
        (marca, modelo, precio, stock)
    )
    conn.commit()
    conn.close()

def eliminar_producto(id_producto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conn.commit()
    conn.close()

def actualizar_producto(id_producto, marca, modelo, precio, stock):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET marca = %s, modelo = %s, precio = %s, stock = %s WHERE id_producto = %s",
        (marca, modelo, precio, stock, id_producto)
    )
    conn.commit()
    conn.close()

def buscar_productos(marca):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_producto, marca, modelo, precio, stock FROM productos WHERE marca LIKE %s",
        ('%' + marca + '%',)
    )
    filas = cursor.fetchall()
    conn.close()
    return [Producto(*fila) for fila in filas]
