/*
*    JS para el landing page de la app de la empresa
*   @autor: Gh0st
*   @version: 1.0
*/


//Inicializacion de var, objetos, DOM

var btnUsuario;
var btnEmpresa;


function domReady(){
    btnUsuario = document.getElementById('btnUsuario');
    btnEmpresa = document.getElementById('btnEmpresa');
    btnUsuario.addEventListener('click', function(){
        window.location.href = 'welcome';
    });
    btnEmpresa.addEventListener('click', function(){
        window.location.href = 'welcome_worker';
    });
}

document.addEventListener('DOMContentLoaded',domReady);