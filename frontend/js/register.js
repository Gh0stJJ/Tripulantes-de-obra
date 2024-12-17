document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Captura de valores por ID
    const full_name = document.getElementById('full_name').value;
    const birth_date = document.getElementById('birth_date').value;
    const national_id = document.getElementById('national_id').value;
    const phone = document.getElementById('phone').value;
    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const repeat_password = document.getElementById('repeat_password').value;

    if (password !== repeat_password) {
        alert("Las contraseñas no coinciden");
        return;
    }

    // Envío de datos al backend
    const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            full_name, birth_date, national_id, phone, email, username, password
        }),
    });

    const result = await response.json();
    if (response.ok) {
        alert('Registro exitoso');
        window.location.href = '/login';
    } else {
        alert(`Error: ${result.message}`);
    }
});
