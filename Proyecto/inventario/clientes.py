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
        "INSERT INTO clientes (nombre, mail, telefono) VALUES (?, ?, ?)",
        (nombre, mail, telefono)
    )
    conn.commit()
    conn.close()

def eliminar_cliente(id_cliente):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))
    conn.commit()
    conn.close()

def actualizar_cliente(id_cliente, nombre, mail, telefono):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clientes SET nombre = ?, mail = ?, telefono = ? WHERE id_cliente = ?",
        (nombre, mail, telefono, id_cliente)
    )
    conn.commit()
    conn.close()
