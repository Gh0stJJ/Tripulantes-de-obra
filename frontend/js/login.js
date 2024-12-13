/*
*    JS para el login de la app con rol de usuario
*   @autor: Gh0st
*   @version: 1.0
*/

//Inicializacion de var, objetos, DOM

var txtusername;
var txtpassword;
var btnLogin;

function domReady(){
    txtusername = document.getElementById('txtusername');
    txtpassword = document.getElementById('txtpassword');
    btnLogin = document.getElementById('btnLogin');
    btnLogin.addEventListener('click', function(){
        if(txtusername.value === 'admin' && txtpassword.value === 'admin'){
            window.location.href = 'welcome.html';
        }else{
            alert('Usuario o contraseña incorrectos');
        }
    });
}
