// Selección de elementos
const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');
const btnEnviar = document.getElementById('btnEnviar');

// Expresiones regulares para validaciones
const expresiones = {
    nombre: /^[a-zA-ZÀ-ÿ\s]{3,40}$/, // mínimo 3 letras
    correo: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, // formato email
    password: /^(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$/ // mínimo 8, un número y un especial
};

// Estado de los campos
const campos = {
    nombre: false,
    correo: false,
    password: false,
    password2: false,
    edad: false
};

// Función para validar cada campo
const validarFormulario = (e) => {
    switch (e.target.name) {
        case "nombre":
            validarCampo(expresiones.nombre, e.target, 'nombre');
        break;
        case "correo":
            validarCampo(expresiones.correo, e.target, 'correo');
        break;
        case "password":
            validarCampo(expresiones.password, e.target, 'password');
            validarPassword2();
        break;
        case "password2":
            validarPassword2();
        break;
        case "edad":
            validarEdad(e.target);
        break;
    }
    habilitarBoton();
};

// Validar con regex

const validarCampo = (expresion, input, campo) => {
    if(expresion.test(input.value)){
        // ✅ Aplica clase al input
        input.classList.remove('formulario__input-incorrecto');
        input.classList.add('formulario__input-correcto');

        // Oculta mensaje de error
        document.querySelector(`#grupo__${campo} .formulario__input-error`)
                .classList.remove('formulario__input-error-activo');
        campos[campo] = true;
    } else {
        // ❌ Aplica clase al input
        input.classList.add('formulario__input-incorrecto');
        input.classList.remove('formulario__input-correcto');

        // Muestra mensaje de error
        document.querySelector(`#grupo__${campo} .formulario__input-error`)
                .classList.add('formulario__input-error-activo');
        campos[campo] = false;
    }
};


// Validar confirmación de contraseña
const validarPassword2 = () => {
    const inputPassword1 = document.getElementById('password');
    const inputPassword2 = document.getElementById('password2');

    if(inputPassword1.value === inputPassword2.value && inputPassword2.value !== ""){
        inputPassword2.classList.remove('formulario__input-incorrecto');
        inputPassword2.classList.add('formulario__input-correcto');
        document.querySelector('#grupo__password2 .formulario__input-error')
                .classList.remove('formulario__input-error-activo');
        campos['password2'] = true;
    } else {
        inputPassword2.classList.add('formulario__input-incorrecto');
        inputPassword2.classList.remove('formulario__input-correcto');
        document.querySelector('#grupo__password2 .formulario__input-error')
                .classList.add('formulario__input-error-activo');
        campos['password2'] = false;
    }
};


// Validar edad

const validarEdad = (input) => {
    const edad = parseInt(input.value);
    if(edad >= 18){
      
        input.classList.remove('formulario__input-incorrecto');
        input.classList.add('formulario__input-correcto');

        document.querySelector('#grupo__edad .formulario__input-error')
                .classList.remove('formulario__input-error-activo');
        campos['edad'] = true;
    } else {
        
        input.classList.add('formulario__input-incorrecto');
        input.classList.remove('formulario__input-correcto');

       
        document.querySelector('#grupo__edad .formulario__input-error')
                .classList.add('formulario__input-error-activo');
        campos['edad'] = false;
    }
};

// Habilitar botón si todo es válido
const habilitarBoton = () => {
    const todoValido = Object.values(campos).every(valor => valor === true);
    btnEnviar.disabled = !todoValido;
};

// Eventos en inputs
inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormulario);
    input.addEventListener('blur', validarFormulario);
});

// Evento submit
formulario.addEventListener('submit', (e) => {
    e.preventDefault();
    if(Object.values(campos).every(valor => valor === true)){
        document.getElementById('formulario__mensaje-exito').classList.add('formulario__mensaje-exito-activo');
        document.getElementById('formulario__mensaje').classList.remove('formulario__mensaje-activo');
        alert("Formulario enviado con éxito ✅");
        formulario.reset();
        btnEnviar.disabled = true;
        // Resetear estados
        Object.keys(campos).forEach(campo => campos[campo] = false);
    } else {
        document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');
    }
});

formulario.addEventListener('reset', () => {
    
    inputs.forEach((input) => {
        input.classList.remove('formulario__input-correcto');
        input.classList.remove('formulario__input-incorrecto');
    });

   
    document.getElementById('formulario__mensaje-exito').classList.remove('formulario__mensaje-exito-activo');
    document.getElementById('formulario__mensaje').classList.remove('formulario__mensaje-activo');

    
    btnEnviar.disabled = true;

   
    Object.keys(campos).forEach(campo => campos[campo] = false);
});

