document.getElementById("profession-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const description = document.getElementById("description").value;
    const location = document.getElementById("location").value;
    const phone = document.getElementById("phone").value;
    const instagram = document.getElementById("instagram").value;
    const facebook = document.getElementById("facebook").value;
    const link = document.getElementById("link").value;

    try {
        const response = await fetch("/profession_form", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ description, location, phone, instagram, facebook, link }),
        });

        const result = await response.json();

        if (response.ok) {
            alert("Perfil actualizado exitosamente");
            window.location.href = "/professions_worker";
        } else {
            alert(`Error: ${result.message}`);
        }
    } catch (error) {
        console.error("Error al actualizar el perfil:", error);
        alert("Ocurrió un error inesperado.");
    }
});
