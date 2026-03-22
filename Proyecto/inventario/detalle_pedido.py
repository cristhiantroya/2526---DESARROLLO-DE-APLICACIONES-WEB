from conexion.conexion import get_db_connection

class DetallePedido:
    def __init__(self, id_detalle, id_pedido, id_producto, cantidad, subtotal):
        self.id_detalle = id_detalle
        self.id_pedido = id_pedido
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.subtotal = subtotal

    def __str__(self):
        return f"Detalle {self.id_detalle} - Pedido {self.id_pedido} | Producto {self.id_producto} | Cantidad: {self.cantidad} | Subtotal: {self.subtotal}"

# --- Funciones CRUD ---

def listar_detalles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_detalle, id_pedido, id_producto, cantidad, subtotal FROM detalle_pedido")
    filas = cursor.fetchall()
    conn.close()
    return [DetallePedido(*fila) for fila in filas]

def insertar_detalle(id_pedido, id_producto, cantidad, subtotal):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)",
        (id_pedido, id_producto, cantidad, subtotal)
    )
    conn.commit()
    conn.close()

def eliminar_detalle(id_detalle):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM detalle_pedido WHERE id_detalle = ?", (id_detalle,))
    conn.commit()
    conn.close()

def actualizar_detalle(id_detalle, id_pedido, id_producto, cantidad, subtotal):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE detalle_pedido SET id_pedido = ?, id_producto = ?, cantidad = ?, subtotal = ? WHERE id_detalle = ?",
        (id_pedido, id_producto, cantidad, subtotal, id_detalle)
    )
    conn.commit()
    conn.close()
