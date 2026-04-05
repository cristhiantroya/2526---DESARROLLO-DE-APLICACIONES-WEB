from conexion.conexion import get_db_connection

class Cliente:
    def __init__(self, id_cliente, nombre, mail, telefono):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.mail = mail
        self.telefono = telefono

    def __str__(self):
        return f"{self.id_cliente} - {self.nombre} | Mail: {self.mail} | Teléfono: {self.telefono}"

# --- Funciones CRUD ---

def listar_clientes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nombre, mail, telefono FROM clientes")
    filas = cursor.fetchall()
    conn.close()
    return [Cliente(*fila) for fila in filas]

def insertar_cliente(nombre, mail, telefono):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clientes (nombre, mail, telefono) VALUES (%s, %s, %s)",
        (nombre, mail, telefono)
    )
    conn.commit()
    conn.close()

def eliminar_cliente(id_cliente):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
    conn.commit()
    conn.close()

def obtener_cliente(id_cliente):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nombre, mail, telefono FROM clientes WHERE id_cliente = %s", (id_cliente,))
    fila = cursor.fetchone()
    conn.close()
    if fila:
        return Cliente(*fila)
    return None


def actualizar_cliente(id_cliente, nombre, mail, telefono):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clientes SET nombre = %s, mail = %s, telefono = %s WHERE id_cliente = %s",
        (nombre, mail, telefono, id_cliente)
    )
    conn.commit()
    conn.close()


def contar_clientes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def listar_clientes_paginados(offset, limit):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nombre, mail, telefono FROM clientes ORDER BY id_cliente LIMIT %s OFFSET %s", (limit, offset))
    filas = cursor.fetchall()
    conn.close()
    return [Cliente(*fila) for fila in filas]


def buscar_clientes(nombre, offset, limit):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nombre, mail, telefono FROM clientes WHERE nombre LIKE %s ORDER BY id_cliente LIMIT %s OFFSET %s", ('%' + nombre + '%', limit, offset))
    filas = cursor.fetchall()
    conn.close()
    return [Cliente(*fila) for fila in filas]


def contar_clientes_busqueda(nombre):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes WHERE nombre LIKE %s", ('%' + nombre + '%',))
    total = cursor.fetchone()[0]
    conn.close()
    return total
