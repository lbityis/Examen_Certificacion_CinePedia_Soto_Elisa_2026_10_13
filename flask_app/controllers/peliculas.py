from flask import render_template, request, redirect, url_for, session
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario

@app.route("/cine")
def dashboard():
    # Proteger ruta para usuarios logueados
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    # Cargar la lista completa de peliculas
    peliculas = Pelicula.obtener_todas()
    return render_template("usuarios.html", peliculas=peliculas)

@app.route("/cine/nueva")
def nueva_pelicula():
    # Formulario para registrar una pelicula
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    return render_template("nueva_pelicula.html", datos_previos={})

@app.route("/cine/crear", methods=["POST"])
def crear_pelicula():
    # Procesar creacion de la pelicula
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    # Si hay error, se mantiene la sinopsis e informacion cargada
    if not Pelicula.validar_pelicula(request.form):
        return render_template("nueva_pelicula.html", datos_previos=request.form)

    datos = {
        "titulo": request.form["titulo"].strip(),
        "director": request.form["director"].strip(),
        "fecha_estreno": request.form["fecha_estreno"],
        "sinopsis": request.form["sinopsis"].strip(),
        "usuario_id": session["usuario_id"]
    }

    Pelicula.guardar(datos)
    return redirect(url_for("dashboard"))

@app.route("/cine/<int:id>")
def ver_pelicula(id):
    # Ver detalle individual y lista de comentarios
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    pelicula = Pelicula.obtener_por_id(id)
    if not pelicula:
        return redirect(url_for("dashboard"))

    comentarios = Comentario.obtener_por_pelicula(id)
    return render_template("ver_pelicula.html", pelicula=pelicula, comentarios=comentarios)

@app.route("/cine/editar/<int:id>")
def editar_pelicula(id):
    # Formulario para editar pelicula
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    pelicula = Pelicula.obtener_por_id(id)
    # Verificar que solo el creador pueda ingresar
    if not pelicula or pelicula.usuario_id != session["usuario_id"]:
        return redirect(url_for("dashboard"))

    return render_template("editar_pelicula.html", pelicula=pelicula, datos_previos={})

@app.route("/cine/actualizar/<int:id>", methods=["POST"])
def actualizar_pelicula(id):
    # Guardar cambios de la edicion
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    pelicula = Pelicula.obtener_por_id(id)
    if not pelicula or pelicula.usuario_id != session["usuario_id"]:
        return redirect(url_for("dashboard"))

    if not Pelicula.validar_pelicula(request.form, pelicula_id=id):
        return render_template("editar_pelicula.html", pelicula=pelicula, datos_previos=request.form)

    datos = {
        "id": id,
        "titulo": request.form["titulo"].strip(),
        "director": request.form["director"].strip(),
        "fecha_estreno": request.form["fecha_estreno"],
        "sinopsis": request.form["sinopsis"].strip()
    }

    Pelicula.actualizar(datos)
    return redirect(url_for("dashboard"))

@app.route("/cine/borrar/<int:id>")
def borrar_pelicula(id):
    # Eliminar pelicula si pertenece al usuario en sesion
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    pelicula = Pelicula.obtener_por_id(id)
    if pelicula and pelicula.usuario_id == session["usuario_id"]:
        Pelicula.eliminar(id)

    return redirect(url_for("dashboard"))