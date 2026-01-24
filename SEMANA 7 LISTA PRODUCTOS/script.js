// arreglo de productos inicial
let productos = [
    { nombre: "Samsung Samsung Galaxy S25 Ultra ", precio: 1200, descripcion: "Teléfono gama alta con cámara profesional" },
    { nombre: "Apple iPhone 17 Pro ", precio: 1800, descripcion: "Smartphone premium enfocado en ecosistema iOS." },
    { nombre: "Google Pixel 10 Pro", precio: 1600, descripcion: "Celular con IA avanzada y fotografía pura." },
    { nombre: "Xiaomi 15 Ultra ", precio: 1000, descripcion: "Gama alta con carga ultrarrápida y gran batería." },
    { nombre: "OnePlus 13", precio: 900, descripcion: "Teléfono potente para gaming y rendimiento fluido." },
    { nombre: "Oppo Find X9 Pro", precio: 850, descripcion: "Cámara Hasselblad y diseño elegante de gama alta." },
    { nombre: "Vivo X300 Pro", precio: 1020, descripcion: " Especialista en fotos con zoom extremo." },
    { nombre: "Samsung Galaxy A56", precio: 350, descripcion: "Teléfono gama media equilibrado con actualizaciones largas." },
    { nombre: "Poco X8 Pro ", precio: 250, descripcion: "Celular gamer económico con alto rendimiento." },
    { nombre: "Motorola Edge 50 Pro ", precio: 450, descripcion: "Gama media con pantalla curva y buen audio." },
];

// función para renderizar productos en la lista
function mostrarProductos() {
    let lista = document.getElementById("lista-productos");
    if (!lista) {
        console.error("No se encontró el elemento lista-productos");
        return;
    }
    lista.innerHTML = ""; 

    for (let i = 0; i < productos.length; i++) {
        let item = document.createElement("li");
        item.textContent = productos[i].nombre + " - $" + productos[i].precio + " - " + productos[i].descripcion;
        lista.appendChild(item);
    }
}

// función para agregar un producto nuevo
function agregarProducto() {
    console.log("Botón clickeado"); // Para debug
    
    const nombre = prompt("Ingrese el nombre del producto:");
    const precioStr = prompt("Ingrese el precio del producto:");
    const precio = parseFloat(precioStr);
    const descripcion = prompt("Ingrese la descripción del producto:");
    
    console.log("Datos:", nombre, precio, descripcion); // Para debug
    
    if (nombre && !isNaN(precio) && descripcion) {
        const nuevoProducto = {
            nombre: nombre,
            precio: precio,
            descripcion: descripcion
        };
        productos.push(nuevoProducto);
        console.log("Producto agregado:", nuevoProducto); // Para debug
        mostrarProductos();
        alert("¡Producto agregado correctamente!");
    } else {
        alert("Datos inválidos. Intente nuevamente.");
    }
}

// cuando cargue la página, mostrar productos
window.onload = function() {
    console.log("Página cargada");
    mostrarProductos();
    const btn = document.getElementById("btn-agregar");
    if (btn) {
        btn.onclick = agregarProducto;
        console.log("Botón configurado");
    } else {
        console.error("No se encontró el botón btn-agregar");
    }
};