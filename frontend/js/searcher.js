document.addEventListener("DOMContentLoaded", () => {
    // Seleccionar todas las tarjetas de profesionales
    const professionalCards = document.querySelectorAll(".professional-card");

    // Agregar evento de clic a cada tarjeta
    professionalCards.forEach((card) => {
        card.addEventListener("click", () => {
            const professionalId = card.getAttribute("data-id");
            const profession = card.getAttribute("data-profession");
            console.log(professionalId, profession);
            if (professionalId && profession) {
                // Redirigir a la página de detalles del profesional
                window.location.href = `/professionals/${profession}/${professionalId}`;
            } else {
                console.error("Datos del profesional no encontrados.");
            }
        });
    });
});
