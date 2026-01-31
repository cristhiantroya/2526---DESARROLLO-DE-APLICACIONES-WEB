// Botón de alerta
document.getElementById("alertBtn").addEventListener("click", function() {
  alert("¡Hola! Esta es una alerta personalizada :)");
});

// Validación del formulario
document.getElementById("contactForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Evita que se envíe sin validar

  let nombre = document.getElementById("nombre").value.trim();
  let correo = document.getElementById("correo").value.trim();
  let mensaje = document.getElementById("mensaje").value.trim();

  if (nombre === "" || correo === "" || mensaje === "") {
    alert("Por favor, completa todos los campos antes de enviar.");
  } else {
    alert("Formulario enviado correctamente. ¡Gracias por tu mensaje!");
    // Aquí podrías resetear el formulario si quieres
    document.getElementById("contactForm").reset();
  }
});
