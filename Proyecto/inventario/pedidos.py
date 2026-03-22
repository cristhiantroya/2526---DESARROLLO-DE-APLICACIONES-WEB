from conexion.conexion import get_db_connection

class Pedido:
    def __init__(self, id_pedido, id_cliente, fecha, total):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.fecha = fecha
        self.total = total

    def __str__(self):
        return f"Pedido {self.id_pedido} - Cliente {self.id_cliente} | Fecha: {self.fecha} | Total: {self.total}"

# --- Funciones CRUD ---

def listar_pedidos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_pedido, id_cliente, fecha, total FROM pedidos")
    filas = cursor.fetchall()
    conn.close()
    return [Pedido(*fila) for fila in filas]

def insertar_pedido(id_cliente, fecha, total):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pedidos (id_cliente, fecha, total) VALUES (?, ?, ?)",
        (id_cliente, fecha, total)
    )
    conn.commit()
    conn.close()

def eliminar_pedido(id_pedido):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id_pedido = ?", (id_pedido,))
    conn.commit()
    conn.close()

def actualizar_pedido(id_pedido, id_cliente, fecha, total):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pedidos SET id_cliente = ?, fecha = ?, total = ? WHERE id_pedido = ?",
        (id_cliente, fecha, total, id_pedido)
    )
    conn.commit()
    conn.close()
