"""
Script para inicializar la base de datos con la tabla usuarios
Ejecutar antes de usar la aplicación
"""

from conexion.conexion import get_db_connection

def crear_tabla_usuarios():
    """Crea la tabla usuarios si no existe"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Crear tabla usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        print("✅ Tabla 'usuarios' creada/verificada correctamente")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al crear la tabla: {e}")
        return False


def verificar_estructura_bd():
    """Verifica que la base de datos tenga la estructura correcta"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener información de las columnas
        cursor.execute("""
            SELECT COLUMN_NAME, COLUMN_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'usuarios' AND TABLE_SCHEMA = DATABASE()
        """)
        
        columnas = cursor.fetchall()
        
        if not columnas:
            print("⚠️  La tabla 'usuarios' no existe. Créala ejecutando: python -c 'from database_init import crear_tabla_usuarios; crear_tabla_usuarios()'")
            conn.close()
            return False
        
        print("\n📋 Estructura de la tabla 'usuarios':")
        for col_name, col_type in columnas:
            print(f"   - {col_name}: {col_type}")
        
        required_columns = ['id_usuario', 'nombre', 'email', 'password']
        existing_columns = [col[0] for col in columnas]
        
        missing = [col for col in required_columns if col not in existing_columns]
        
        if missing:
            print(f"\n❌ Faltan columnas: {missing}")
            conn.close()
            return False
        
        print("✅ La estructura de la base de datos es correcta\n")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar la estructura: {e}")
        return False


if __name__ == '__main__':
    print("🔧 Inicializando base de datos...\n")
    
    # Crear tabla
    crear_tabla_usuarios()
    
    # Verificar estructura
    verificar_estructura_bd()
    
    print("\n✨ Inicialización completada")
