document.addEventListener("DOMContentLoaded", function() {
    //validTokenSession();

    token=getCookie('jwt');
    decodedToken=parseJwt(token);
    username=decodedToken.sub;
    rol=decodedToken.rol;
    // Actualizar el contenido del elemento <span> con el nombre de usuario
    document.querySelector('.username').textContent = "Usuario: "+username;
    document.querySelector('.rol').textContent = "Rol: "+rol;


});
