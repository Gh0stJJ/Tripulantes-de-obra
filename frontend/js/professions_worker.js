document.addEventListener("DOMContentLoaded", () => {
    // Seleccionar todos los botones de profesiones
    const professionButtons = document.querySelectorAll(".profession-btn");

    // Agregar evento de clic a cada botón
    professionButtons.forEach((button) => {
        button.addEventListener("click", () => {
            // Obtener la profesión desde el atributo data-profession
            const profession = button.getAttribute("data-profession");

            // Redirigir a la página de profesionales
            if (profession) {
                window.location.href = `/professionals/${profession}`;
            } else {
                console.error("Profesión no encontrada.");
            }
        });
    });
});
