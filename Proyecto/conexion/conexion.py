import mariadb

def get_db_connection():
    try:
        conexion = mariadb.connect(
            host="localhost",
            user="root",
            password="123456",
            database="tienda_celulares"
        )
        print("✅ Conexión exitosa a la base de datos")
        return conexion
    except mysql.connector.Error as error:
        print("❌ Error al conectar a la base de datos:", error)
        return None


