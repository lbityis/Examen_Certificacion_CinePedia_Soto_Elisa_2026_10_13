from flask import request, redirect, url_for, session
from flask_app import app
from flask_app.models.comentario import Comentario
from flask_app.models.pelicula import Pelicula

@app.route("/comentario/crear/<int:pelicula_id>", methods=["POST"])
def crear_comentario(pelicula_id):
    # Agregar un nuevo comentario
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    contenido = request.form.get("contenido", "").strip()
    pelicula = Pelicula.obtener_por_id(pelicula_id)

    # Validar que el creador no pueda comentar su propia peli
    if pelicula and pelicula.usuario_id != session["usuario_id"] and len(contenido) > 0:
        datos = {
            "contenido": contenido,
            "usuario_id": session["usuario_id"],
            "pelicula_id": pelicula_id
        }
        Comentario.guardar(datos)

    return redirect(url_for("ver_pelicula", id=pelicula_id))

@app.route("/comentario/borrar/<int:comentario_id>/<int:pelicula_id>")
def borrar_comentario(comentario_id, pelicula_id):
    # Eliminar comentario solo si le pertenece al usuario
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    comentario = Comentario.obtener_por_id(comentario_id)
    if comentario and comentario.usuario_id == session["usuario_id"]:
        Comentario.eliminar(comentario_id)

    return redirect(url_for("ver_pelicula", id=pelicula_id))