import { API_CONFIG, fetchApi } from '../../../js/config.js';

document.addEventListener('DOMContentLoaded', function () {
    validarSesionAdmin();
    cargarUsuarios();
});

function validarSesionAdmin() {
    const role = localStorage.getItem('role');
    if (role !== 'admin') {
        window.location.href = '../../login_administrador/pages/index.html';
        return;
    }
}

async function cargarUsuarios() {
    try {
        const response = await fetchApi(API_CONFIG.ENDPOINTS.AUTH.USUARIOS, {
            method: 'GET'
        });
        mostrarUsuarios(response.usuarios || []);
    } catch (error) {
        console.error('Error al cargar los usuarios:', error);
        mostrarMensajeError('Error al cargar los usuarios');
    }
}

async function eliminarUsuario(idUsuario) {
    if (!confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
        return;
    }

    try {
        await fetchApi(`${API_CONFIG.ENDPOINTS.AUTH.USUARIOS}/${idUsuario}`, {
            method: 'DELETE'
        });
        mostrarMensajeExito('Usuario eliminado exitosamente');
        cargarUsuarios();
    } catch (error) {
        console.error('Error al eliminar el usuario:', error);
        mostrarMensajeError('Error al eliminar el usuario');
    }
}

function mostrarUsuarios(usuarios) {
    const tbody = document.getElementById('tbody-usuarios');
    tbody.innerHTML = '';

    usuarios.forEach(usuario => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${usuario.id}</td>
            <td>${usuario.nombre}</td>
            <td>${usuario.rol}</td>
            <td>
                <a class="btn btn-primary btn-editar" href="editarUsuario.html?id=${usuario.id}&nombre=${encodeURIComponent(usuario.nombre)}&rol=${encodeURIComponent(usuario.rol)}">
                    <i class="fa-solid fa-pen-to-square"></i> Editar
                </a>
                <button class="btn btn-danger btn-eliminar" data-id="${usuario.id}">
                    <i class="fa-solid fa-trash"></i> Eliminar
                </button>
            </td>
        `;
        tbody.appendChild(row);

        // Agregar evento al botón de eliminar
        const btnEliminar = row.querySelector('.btn-eliminar');
        btnEliminar.addEventListener('click', () => eliminarUsuario(usuario.id));
    });
}

function mostrarMensajeError(mensaje) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.container').prepend(alertDiv);
}

function mostrarMensajeExito(mensaje) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.container').prepend(alertDiv);
} 