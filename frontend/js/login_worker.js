document.getElementById("login-worker-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/login_worker", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });

        const result = await response.json();

        if (response.ok) {
            alert("Inicio de sesión exitoso");
            window.location.href = "/profession_form"; // Redirigir al área de profesionales
        } else {
            alert(`Error: ${result.message}`);
        }
    } catch (error) {
        console.error("Error al iniciar sesión:", error);
        alert("Ocurrió un error al conectar con el servidor.");
    }
});
