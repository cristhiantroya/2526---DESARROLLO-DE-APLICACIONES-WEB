from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from form import ProductoForm, LoginForm, RegistroForm
from models import User, load_user, obtener_usuario_por_email
from inventario import productos  
from inventario import clientes
from inventario import pedidos
from inventario import detalle_pedido
from inventario import usuarios

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_segura'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Ruta a la que se redirige si no está autenticado
login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'

@login_manager.user_loader
def manager_load_user(id_usuario):
    """Carga el usuario desde la base de datos"""
    return load_user(id_usuario)


# ==================== RUTAS DE AUTENTICACIÓN ====================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Ruta para registrar un nuevo usuario"""
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        # Crear un usuario nuevo
        if usuarios.insertar_usuario(form.nombre.data, form.email.data, form.password.data):
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error al registrar el usuario. Intenta nuevamente.', 'danger')
    
    return render_template('registro.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta para iniciar sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Buscar el usuario por email
        usuario = obtener_usuario_por_email(form.email.data)
        
        if usuario and usuario.check_password(form.password.data):
            # Autenticar el usuario
            login_user(usuario)
            flash(f'¡Bienvenido {usuario.nombre}!', 'success')
            
            # Redirigir a la página que intentó acceder o al inicio
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('inicio'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')
    
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Ruta para cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('inicio'))


# ==================== RUTAS PÚBLICAS ====================

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


# ==================== RUTAS PROTEGIDAS - PRODUCTOS ====================
    
@app.route('/productos')
@login_required
def productos_view():
    lista = productos.listar_productos()
    return render_template('productos.html', productos=lista)

@app.route('/agregar_producto', methods=['GET', 'POST'])
@login_required
def agregar_producto():
    form = ProductoForm()
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        stock = request.form['stock']
        productos.insertar_producto(marca, modelo, precio, stock)
        flash('Producto agregado correctamente.', 'success')
        return redirect(url_for('productos_view'))
    return render_template('producto_form.html', form=form)

@app.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    productos.eliminar_producto(id)
    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('productos_view'))

@app.route('/actualizar/<int:id>', methods=['GET', 'POST'])
@login_required
def actualizar(id):
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        stock = request.form['stock']
        productos.actualizar_producto(id, marca, modelo, precio, stock)
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('productos_view'))
    return render_template('producto_form.html')


@app.route('/buscar', methods=['POST'])
@login_required
def buscar():
    nombre = request.form['nombre']
    resultados = productos.buscar_productos(nombre)
    return render_template('productos.html', productos=resultados)


# ==================== RUTAS PROTEGIDAS - CLIENTES ====================

@app.route('/clientes')
@login_required
def clientes_view():
    lista = clientes.listar_clientes()
    return render_template('clientes.html', clientes=lista)

@app.route('/agregar_cliente', methods=['GET', 'POST'])
@login_required
def agregar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        mail = request.form['mail']
        telefono = request.form['telefono']
        clientes.insertar_cliente(nombre, mail, telefono)
        flash('Cliente agregado correctamente.', 'success')
        return redirect(url_for('clientes_view'))
    return render_template('cliente_form.html')

@app.route('/eliminar_cliente/<int:id_cliente>')
@login_required
def eliminar_cliente(id_cliente):
    clientes.eliminar_cliente(id_cliente)
    flash('Cliente eliminado correctamente.', 'success')
    return redirect(url_for('clientes_view'))

@app.route('/actualizar_cliente/<int:id_cliente>', methods=['GET', 'POST'])
@login_required
def actualizar_cliente(id_cliente):
    if request.method == 'POST':
        nombre = request.form['nombre']
        mail = request.form['mail']
        telefono = request.form['telefono']
        clientes.actualizar_cliente(id_cliente, nombre, mail, telefono)
        flash('Cliente actualizado correctamente.', 'success')
        return redirect(url_for('clientes_view'))
    return render_template('cliente_form.html')


# ==================== RUTAS PROTEGIDAS - PEDIDOS ====================

@app.route('/pedidos')
@login_required
def pedidos_view():
    lista = pedidos.listar_pedidos()
    return render_template('pedidos.html', pedidos=lista)

@app.route('/agregar_pedido', methods=['GET', 'POST'])
@login_required
def agregar_pedido():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        fecha = request.form['fecha']
        total = request.form['total']
        pedidos.insertar_pedido(id_cliente, fecha, total)
        flash('Pedido agregado correctamente.', 'success')
        return redirect(url_for('pedidos_view'))
    return render_template('pedido_form.html')

@app.route('/eliminar_pedido/<int:id_pedido>')
@login_required
def eliminar_pedido(id_pedido):
    pedidos.eliminar_pedido(id_pedido)
    flash('Pedido eliminado correctamente.', 'success')
    return redirect(url_for('pedidos_view'))

@app.route('/actualizar_pedido/<int:id_pedido>', methods=['GET', 'POST'])
@login_required
def actualizar_pedido(id_pedido):
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        fecha = request.form['fecha']
        total = request.form['total']
        pedidos.actualizar_pedido(id_pedido, id_cliente, fecha, total)
        flash('Pedido actualizado correctamente.', 'success')
        return redirect(url_for('pedidos_view'))
    return render_template('pedido_form.html')


# ==================== RUTAS PROTEGIDAS - DETALLES ====================

@app.route('/detalle_pedido')
@login_required
def detalle_view():
    lista = detalle_pedido.listar_detalles()
    return render_template('detalle_pedido.html', detalles=lista)

@app.route('/agregar_detalle', methods=['GET', 'POST'])
@login_required
def agregar_detalle():
    if request.method == 'POST':
        id_pedido = request.form['id_pedido']
        id_producto = request.form['id_producto']
        cantidad = request.form['cantidad']
        subtotal = request.form['subtotal']
        detalle_pedido.insertar_detalle(id_pedido, id_producto, cantidad, subtotal)
        flash('Detalle agregado correctamente.', 'success')
        return redirect(url_for('detalle_view'))
    return render_template('detalle_form.html')

@app.route('/eliminar_detalle/<int:id_detalle>')
@login_required
def eliminar_detalle(id_detalle):
    detalle_pedido.eliminar_detalle(id_detalle)
    flash('Detalle eliminado correctamente.', 'success')
    return redirect(url_for('detalle_view'))

@app.route('/actualizar_detalle/<int:id_detalle>', methods=['GET', 'POST'])
@login_required
def actualizar_detalle(id_detalle):
    if request.method == 'POST':
        id_pedido = request.form['id_pedido']
        id_producto = request.form['id_producto']
        cantidad = request.form['cantidad']
        subtotal = request.form['subtotal']
        detalle_pedido.actualizar_detalle(id_detalle, id_pedido, id_producto, cantidad, subtotal)
        flash('Detalle actualizado correctamente.', 'success')
        return redirect(url_for('detalle_view'))
    return render_template('detalle_form.html')


# ==================== RUTAS PROTEGIDAS - USUARIOS ====================

@app.route('/usuarios')
@login_required
def usuarios_view():
    lista = usuarios.listar_usuarios()
    return render_template('usuarios.html', usuarios=lista)

@app.route('/agregar_usuario', methods=['GET', 'POST'])
@login_required
def agregar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        usuarios.insertar_usuario(nombre, email, password)
        flash('Usuario agregado correctamente.', 'success')
        return redirect(url_for('usuarios_view'))
    return render_template('usuario_form.html')

@app.route('/eliminar_usuario/<int:id_usuario>')
@login_required
def eliminar_usuario(id_usuario):
    usuarios.eliminar_usuario(id_usuario)
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('usuarios_view'))

@app.route('/actualizar_usuario/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def actualizar_usuario(id_usuario):
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        usuarios.actualizar_usuario(id_usuario, nombre, email, password)
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('usuarios_view'))
    return render_template('usuario_form.html')


# ==================== RUTAS UTILITARIAS ====================

@app.route('/db_test')
def db_test():
    try:
        lista = productos.listar_productos()
        return "✅ Conexión a la base de datos exitosa"
    except Exception as e:
        return f"❌ Error al conectar a la base de datos: {e}"

if __name__ == '__main__':
    app.run(debug=True)



