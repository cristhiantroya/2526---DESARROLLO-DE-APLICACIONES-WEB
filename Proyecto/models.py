from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from conexion.conexion import get_db_connection


class User(UserMixin):
    """Clase Usuario compatible con Flask-Login"""
    
    def __init__(self, id_usuario, nombre, email, password=None):
        self.id = id_usuario  # Flask-Login requiere 'id'
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password
    
    def __str__(self):
        return f"{self.id_usuario} - {self.nombre} | Email: {self.email}"
    
    def set_password(self, password):
        """Genera un hash seguro de la contraseña"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica si la contraseña coincide con el hash almacenado"""
        return check_password_hash(self.password, password)


def load_user(id_usuario):
    """Carga un usuario desde la base de datos por ID (requerido por Flask-Login)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario, nombre, email, password FROM usuarios WHERE id_usuario = ?",
            (int(id_usuario),)
        )
        fila = cursor.fetchone()
        conn.close()
        
        if fila is None:
            return None
        
        usuario = User(*fila)
        return usuario
    except Exception as e:
        print(f"Error al cargar usuario: {e}")
        return None


def obtener_usuario_por_email(email):
    """Obtiene un usuario por su email"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario, nombre, email, password FROM usuarios WHERE email = ?",
            (email,)
        )
        fila = cursor.fetchone()
        conn.close()
        
        if fila is None:
            return None
        
        usuario = User(*fila)
        return usuario
    except Exception as e:
        print(f"Error al obtener usuario por email: {e}")
        return None
