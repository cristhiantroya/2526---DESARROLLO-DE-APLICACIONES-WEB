from flask import Flask, render_template, request, redirect, url_for
from form import ProductoForm
from inventario.bd import crear_tablas, conectar
from flask_sqlalchemy import SQLAlchemy 
from inventario.inventario_persistencia import (
    guardar_csv, leer_csv,
    guardar_json, leer_json,
    guardar_txt, leer_txt
)
from conexion.conexion import get_db_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Crear tablas al iniciar
crear_tablas()

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/productos')
def productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        precio = form.precio.data

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                       (nombre, cantidad, precio))
        conn.commit()
        conn.close()

        # Redirige al listado de productos
        return redirect(url_for('productos'))

    return render_template('producto_form.html', form=form)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))

@app.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    producto = cursor.fetchone()

    form = ProductoForm()

    if request.method == 'POST' and form.validate_on_submit():
        nueva_cantidad = form.cantidad.data
        nuevo_precio = form.precio.data
        cursor.execute("UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?",
                       (nueva_cantidad, nuevo_precio, id))
        conn.commit()
        conn.close()
        return redirect(url_for('productos'))

    conn.close()
    return render_template('producto_form.html', form=form, producto=producto)




@app.route('/buscar', methods=['POST'])
def buscar():
    nombre = request.form['nombre']
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
    resultados = cursor.fetchall()
    conn.close()
    return render_template('productos.html', productos=resultados)



@app.route('/datos', methods=['GET', 'POST'])
def datos():
    if request.method == 'POST':
        producto = {
            "nombre": request.form['nombre'],
            "descripcion": request.form['descripcion'],
            "precio": request.form['precio'],
            "cantidad": request.form['cantidad']
        }
        guardar_txt(producto)
        guardar_json(producto)
        guardar_csv(producto)
        return redirect(url_for('datos'))

    datos_txt = leer_txt()
    datos_json = leer_json()
    datos_csv = leer_csv()
    return render_template("datos.html", txt=datos_txt, json=datos_json, csv=datos_csv)


# Ruta de prueba de conexión a la base de datos
@app.route('/db_test')
def db_test():
    print("➡️ Entrando a /db_test")
    try:
        conn = get_db_connection()
        if conn is None:
            return "No se pudo conectar a la base de datos"

        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()

        if result and result[0] == 1:
            return "Conexión a la base de datos exitosa"
        else:
            return "Error en la consulta a la base de datos"
    except Exception as e:
        return f"Error al conectar a la base de datos: {e}"



if __name__ == '__main__':
    app.run(debug=True)

