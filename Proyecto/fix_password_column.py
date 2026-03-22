"""
Script para aumentar el tamaño de la columna password a VARCHAR(255)
"""

from conexion.conexion import get_db_connection

try:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("🔧 Alterando columna 'password' a VARCHAR(255)...")
    
    cursor.execute("""
        ALTER TABLE usuarios 
        MODIFY COLUMN password VARCHAR(255) NOT NULL
    """)
    
    conn.commit()
    print("✅ Columna 'password' alterada correctamente a VARCHAR(255)")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error al alterar la tabla: {e}")
