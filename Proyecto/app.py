from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from form import ProductoForm, LoginForm, RegistroForm
from models import User, load_user, obtener_usuario_por_email
from inventario import productos  
from inventario import clientes
from io import BytesIO
from fpdf import FPDF
import math
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
    if current_user.is_authenticated and not request.args.get('force'):
        # Si el usuario ya está autenticado, mostrar mensaje y opción de logout
        flash('Ya tienes una sesión activa. Cierra sesión para registrar una nueva cuenta.', 'info')
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
    if current_user.is_authenticated and not request.args.get('force'):
        # Si el usuario ya está autenticado, mostrar mensaje y opción de logout
        flash('Ya tienes una sesión activa. Si deseas cambiar de cuenta, cierra sesión primero.', 'info')
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
    # Productos destacados para mostrar en la página de inicio
    productos_destacados = productos.listar_productos()[:6]
    return render_template('index.html', destacados=productos_destacados)

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
    if form.validate_on_submit():
        marca = form.marca.data
        modelo = form.modelo.data
        precio = form.precio.data
        stock = form.stock.data
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
    producto = productos.obtener_producto(id)
    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('productos_view'))

    form = ProductoForm(obj=producto)

    if request.method == 'POST' and form.validate_on_submit():
        marca = form.marca.data
        modelo = form.modelo.data
        precio = form.precio.data
        stock = form.stock.data
        productos.actualizar_producto(id, marca, modelo, precio, stock)
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('productos_view'))

    return render_template('producto_form.html', form=form, producto=producto)


@app.route('/productos/reporte_pdf')
@login_required
def reporte_productos_pdf():
    lista = productos.listar_productos()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Reporte de Productos', ln=True, align='C')
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(20, 10, 'ID', 1)
    pdf.cell(40, 10, 'Marca', 1)
    pdf.cell(50, 10, 'Modelo', 1)
    pdf.cell(30, 10, 'Precio', 1)
    pdf.cell(30, 10, 'Stock', 1)
    pdf.ln()

    pdf.set_font('Arial', '', 12)
    for producto in lista:
        pdf.cell(20, 10, str(producto.id_producto), 1)
        pdf.cell(40, 10, str(producto.marca), 1)
        pdf.cell(50, 10, str(producto.modelo), 1)
        pdf.cell(30, 10, f"${producto.precio}", 1)
        pdf.cell(30, 10, str(producto.stock), 1)
        pdf.ln()

    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin-1'))
    pdf_output.seek(0)

    return send_file(pdf_output,
                     download_name='reporte_productos.pdf',
                     mimetype='application/pdf',
                     as_attachment=True)


@app.route('/clientes/reporte_pdf')
@login_required
def reporte_clientes_pdf():
    lista = clientes.listar_clientes()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Reporte de Clientes', ln=True, align='C')
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(20, 10, 'ID', 1)
    pdf.cell(60, 10, 'Nombre', 1)
    pdf.cell(70, 10, 'Mail', 1)
    pdf.cell(40, 10, 'Teléfono', 1)
    pdf.ln()

    pdf.set_font('Arial', '', 12)
    for c in lista:
        pdf.cell(20, 10, str(c.id_cliente), 1)
        pdf.cell(60, 10, str(c.nombre), 1)
        pdf.cell(70, 10, str(c.mail), 1)
        pdf.cell(40, 10, str(c.telefono), 1)
        pdf.ln()

    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin-1'))
    pdf_output.seek(0)

    return send_file(pdf_output,
                     download_name='reporte_clientes.pdf',
                     mimetype='application/pdf',
                     as_attachment=True)


@app.route('/pedidos/reporte_pdf')
@login_required
def reporte_pedidos_pdf():
    lista = pedidos.listar_pedidos()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Reporte de Pedidos', ln=True, align='C')
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(20, 10, 'ID', 1)
    pdf.cell(30, 10, 'Cliente', 1)
    pdf.cell(40, 10, 'Fecha', 1)
    pdf.cell(30, 10, 'Total', 1)
    pdf.ln()

    pdf.set_font('Arial', '', 12)
    for p in lista:
        pdf.cell(20, 10, str(p.id_pedido), 1)
        pdf.cell(30, 10, str(p.id_cliente), 1)
        pdf.cell(40, 10, str(p.fecha), 1)
        pdf.cell(30, 10, f"${p.total}", 1)
        pdf.ln()

    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin-1'))
    pdf_output.seek(0)

    return send_file(pdf_output,
                     download_name='reporte_pedidos.pdf',
                     mimetype='application/pdf',
                     as_attachment=True)


@app.route('/buscar', methods=['POST'])
@login_required
def buscar():
    marca = request.form['marca']
    resultados = productos.buscar_productos(marca)
    return render_template('productos.html', productos=resultados)


# ==================== RUTAS PROTEGIDAS - CLIENTES ====================

@app.route('/clientes')
@login_required
def clientes_view():
    page = int(request.args.get('page', 1))
    per_page = 10
    q = request.args.get('q', '').strip()

    if q:
        total = clientes.contar_clientes_busqueda(q)
        clientes_list = clientes.buscar_clientes(q, (page - 1) * per_page, per_page)
    else:
        total = clientes.contar_clientes()
        clientes_list = clientes.listar_clientes_paginados((page - 1) * per_page, per_page)

    total_pages = max(1, math.ceil(total / per_page))
    return render_template('clientes.html', clientes=clientes_list, page=page, total_pages=total_pages, q=q)

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
    return render_template('cliente_form.html', cliente=None)

@app.route('/actualizar_cliente/<int:id_cliente>', methods=['GET', 'POST'])
@login_required
def actualizar_cliente(id_cliente):
    cliente = clientes.obtener_cliente(id_cliente)
    if not cliente:
        flash('Cliente no encontrado.', 'danger')
        return redirect(url_for('clientes_view'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        mail = request.form['mail']
        telefono = request.form['telefono']
        clientes.actualizar_cliente(id_cliente, nombre, mail, telefono)
        flash('Cliente actualizado correctamente.', 'success')
        return redirect(url_for('clientes_view'))

    return render_template('cliente_form.html', cliente=cliente)

@app.route('/eliminar_cliente/<int:id_cliente>')
@login_required
def eliminar_cliente(id_cliente):
    clientes.eliminar_cliente(id_cliente)
    flash('Cliente eliminado correctamente.', 'success')
    return redirect(url_for('clientes_view'))

# ==================== RUTAS PROTEGIDAS - PEDIDOS ====================

@app.route('/pedidos')
@login_required
def pedidos_view():
    page = int(request.args.get('page', 1))
    per_page = 10
    id_cliente = request.args.get('id_cliente', '').strip()
    fecha = request.args.get('fecha', '').strip()

    if id_cliente or fecha:
        total = pedidos.contar_pedidos_busqueda(id_cliente if id_cliente else None, fecha if fecha else None)
        pedidos_list = pedidos.buscar_pedidos(id_cliente if id_cliente else None, fecha if fecha else None, (page - 1) * per_page, per_page)
    else:
        total = pedidos.contar_pedidos()
        pedidos_list = pedidos.listar_pedidos_paginados((page - 1) * per_page, per_page)

    total_pages = max(1, math.ceil(total / per_page))
    return render_template('pedidos.html', pedidos=pedidos_list, page=page, total_pages=total_pages, id_cliente=id_cliente, fecha=fecha)

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



