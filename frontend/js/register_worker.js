document.getElementById("register-worker-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const full_name = document.getElementById("full_name").value;
    const birth_date = document.getElementById("birth_date").value;
    const national_id = document.getElementById("national_id").value;
    const phone = document.getElementById("phone").value;
    const profession = document.getElementById("profession").value;
    const email = document.getElementById("email").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const repeat_password = document.getElementById("repeat_password").value;

    if (password !== repeat_password) {
        alert("Las contraseñas no coinciden");
        return;
    }

    try {
        const response = await fetch("/register_worker", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                full_name,
                birth_date,
                national_id,
                phone,
                profession,
                email,
                username,
                password
            }),
        });

        const result = await response.json();
        if (response.ok) {
            alert("Registro exitoso");
            window.location.href = "/welcome_worker";
        } else {
            alert(`Error: ${result.message}`);
        }
    } catch (error) {
        console.error("Error al registrar trabajador:", error);
        alert("Ocurrió un error inesperado");
    }
});
