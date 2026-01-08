// Selección de elementos del DOM
const imageUrlInput = document.getElementById("imageUrl");
const addImageBtn = document.getElementById("addImageBtn");
const deleteImageBtn = document.getElementById("deleteImageBtn");
const gallery = document.getElementById("gallery");

let selectedImage = null;

// Función para agregar imagen
function addImage() {
  const url = imageUrlInput.value.trim();
  if (url) {
    const img = document.createElement("img");
    img.src = url;

    // Evento click para seleccionar imagen
    img.addEventListener("click", () => {
      if (selectedImage) {
        selectedImage.classList.remove("selected");
      }
      img.classList.add("selected");
      selectedImage = img;
    });

    gallery.appendChild(img);
    imageUrlInput.value = ""; // limpiar campo
  }
}

// Función para eliminar imagen seleccionada
function deleteSelectedImage() {
  if (selectedImage) {
    gallery.removeChild(selectedImage);
    selectedImage = null;
  }
}


// Eventos de botones
addImageBtn.addEventListener("click", addImage);
deleteImageBtn.addEventListener("click", deleteSelectedImage);

// Evento input para validar URL
imageUrlInput.addEventListener("input", () => {
  console.log("URL ingresada:", imageUrlInput.value);
});

// Evento de teclado (ejemplo: Enter para agregar imagen)
document.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    addImage();
  }
  
});
