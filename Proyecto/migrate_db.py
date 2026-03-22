"""
Script para migrar la base de datos de 'mail' a 'email'
Ejecutar si la tabla usuarios tiene la columna 'mail' en lugar de 'email'
"""

from conexion.conexion import get_db_connection

def migrar_mail_a_email():
    """Cambia el nombre de la columna mail a email"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si existe la columna mail
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'usuarios' AND TABLE_SCHEMA = DATABASE()
            AND COLUMN_NAME = 'mail'
        """)
        
        if cursor.fetchone():
            print("🔄 Migrando columna 'mail' a 'email'...")
            
            # Cambiar el nombre de la columna
            cursor.execute("""
                ALTER TABLE usuarios 
                CHANGE COLUMN mail email VARCHAR(120) UNIQUE NOT NULL
            """)
            
            conn.commit()
            print("✅ Migración completada exitosamente")
            conn.close()
            return True
        else:
            print("✅ La columna 'email' ya existe, no se requiere migración")
            conn.close()
            return True
            
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False


if __name__ == '__main__':
    print("🔧 Herramienta de Migración de Base de Datos\n")
    migrar_mail_a_email()
