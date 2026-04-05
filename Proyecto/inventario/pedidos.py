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
        "INSERT INTO pedidos (id_cliente, fecha, total) VALUES (%s, %s, %s)",
        (id_cliente, fecha, total)
    )
    conn.commit()
    conn.close()

def eliminar_pedido(id_pedido):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id_pedido = %s", (id_pedido,))
    conn.commit()
    conn.close()


def actualizar_pedido(id_pedido, id_cliente, fecha, total):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pedidos SET id_cliente = %s, fecha = %s, total = %s WHERE id_pedido = %s",
        (id_cliente, fecha, total, id_pedido)
    )
    conn.commit()
    conn.close()


def contar_pedidos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def listar_pedidos_paginados(offset, limit):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_pedido, id_cliente, fecha, total FROM pedidos ORDER BY id_pedido LIMIT %s OFFSET %s", (limit, offset))
    filas = cursor.fetchall()
    conn.close()
    return [Pedido(*fila) for fila in filas]


def buscar_pedidos(id_cliente=None, fecha=None, offset=0, limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT id_pedido, id_cliente, fecha, total FROM pedidos"
    params = []
    filters = []
    if id_cliente:
        filters.append("id_cliente = %s")
        params.append(id_cliente)
    if fecha:
        filters.append("fecha = %s")
        params.append(fecha)
    if filters:
        query += " WHERE " + " AND ".join(filters)
    query += " ORDER BY id_pedido LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    cursor.execute(query, tuple(params))
    filas = cursor.fetchall()
    conn.close()
    return [Pedido(*fila) for fila in filas]


def contar_pedidos_busqueda(id_cliente=None, fecha=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM pedidos"
    params = []
    filters = []
    if id_cliente:
        filters.append("id_cliente = %s")
        params.append(id_cliente)
    if fecha:
        filters.append("fecha = %s")
        params.append(fecha)
    if filters:
        query += " WHERE " + " AND ".join(filters)
    cursor.execute(query, tuple(params))
    total = cursor.fetchone()[0]
    conn.close()
    return total
