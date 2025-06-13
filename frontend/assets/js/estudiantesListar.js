document.addEventListener("DOMContentLoaded", function() {
    var username = getCookie("username");
    if (username) {
        document.getElementById("admin-username").textContent = username;
    }
    fetch(API_URL + "/ia/estudiantes/listar", { headers: { "Authorization": "Bearer " + getCookie("jwt") } })
        .then(response => response.json())
        .then(data => {
            var tbody = document.getElementById("tbody-estudiantes");
            tbody.innerHTML = "";
            data.forEach(est => {
                var fotosHtml = est.fotos.map(fotoUrl => `<img src='${IA_URL + fotoUrl}' alt='foto' style='width:50px;height:50px;object-fit:cover;margin:2px;border-radius:6px;border:1px solid #ccc;'>`).join("");
                tbody.innerHTML += `<tr><td>${est.codigo}</td><td>${fotosHtml}</td></tr>`;
            });
        })
        .catch(error => console.error("Error al cargar el listado:", error));
}); 