document.addEventListener("DOMContentLoaded", function () {
    // Seleccionar todos los botones de profesionales
    const professionalButtons = document.querySelectorAll(".professional-title");

    professionalButtons.forEach(button => {
        button.addEventListener("click", function () {
            // Obtener el valor del atributo data-profession
            const profession = button.getAttribute("data-profession");
            if (profession) {
                // Redirigir a la URL de profesionales
                window.location.href = `/professionals/${profession}`;
            } else {
                console.error("No se encontró la profesión asociada.");
            }
        });
    });
});
