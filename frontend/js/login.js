/*
*    JS para el login de la app con rol de usuario
*   @autor: Gh0st
*   @version: 1.0
*/

//Inicializacion de var, objetos, DOM

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const result = await response.json();

        if (response.ok) {
            alert('Inicio de sesión exitoso');
            window.location.href = '/problems'; // Redirigir en caso de éxito
        } else {
            alert(`Error: ${result.message}`);
        }
    } catch (error) {
        console.error('Error al iniciar sesión:', error);
        alert('Ocurrió un error al conectar con el servidor.');
    }
});
