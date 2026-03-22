from conexion.conexion import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    def __init__(self, id_usuario, nombre, email, password):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    def __str__(self):
        return f"{self.id_usuario} - {self.nombre} | Email: {self.email}"
    
    def check_password(self, password):
        """Verifica si la contraseña coincide con el hash almacenado"""
        return check_password_hash(self.password, password)
    
# --- Funciones CRUD --- 

def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nombre, email, password FROM usuarios")
    filas = cursor.fetchall()
    conn.close()
    return [Usuario(*fila) for fila in filas]

def insertar_usuario(nombre, email, password):
    """Inserta un usuario con contraseña hasheada"""
    try:
        # Hashear la contraseña antes de almacenar
        password_hash = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password_hash)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al insertar usuario: {e}")
        return False

def verificar_credenciales(email, password):
    """Verifica si el email y password son correctos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario, nombre, email, password FROM usuarios WHERE email = %s",
            (email,)
        )
        fila = cursor.fetchone()
        conn.close()
        
        if fila is None:
            return None
        
        usuario = Usuario(*fila)
        # Verificar la contraseña contra el hash almacenado
        if check_password_hash(usuario.password, password):
            return usuario
        return None
    except Exception as e:
        print(f"Error al verificar credenciales: {e}")
        return None

def obtener_usuario_por_id(id_usuario):
    """Obtiene un usuario por ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario, nombre, email, password FROM usuarios WHERE id_usuario = %s",
            (id_usuario,)
        )
        fila = cursor.fetchone()
        conn.close()
        
        if fila is None:
            return None
        return Usuario(*fila)
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        return None

def obtener_usuario_por_email(email):
    """Obtiene un usuario por email"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario, nombre, email, password FROM usuarios WHERE email = %s",
            (email,)
        )
        fila = cursor.fetchone()
        conn.close()
        
        if fila is None:
            return None
        return Usuario(*fila)
    except Exception as e:
        print(f"Error al obtener usuario por email: {e}")
        return None

def eliminar_usuario(id_usuario):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (id_usuario,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return False

def actualizar_usuario(id_usuario, nombre, email, password):
    """Actualiza un usuario, hasheando la contraseña si es necesario"""
    try:
        password_hash = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET nombre = ?, email = ?, password = ? WHERE id_usuario = ?",
            (nombre, email, password_hash, id_usuario)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return False
