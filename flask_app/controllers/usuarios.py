from flask import render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.usuario import Usuario

bcrypt = Bcrypt(app)

@app.route("/registrar", methods=["POST"])
def registrar():
    # Validamos todos los campos del formulario
    if not Usuario.validar_registro(request.form):
        return redirect(url_for("inicio"))

    # Hasheamos la contraseña antes de guardar
    password_hash = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

    datos = {
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip().lower(),
        "password": password_hash,
        "fecha_nacimiento": request.form["fecha_nacimiento"]
    }

    # Guardamos en la bd y guardamos la sesion
    usuario_id = Usuario.guardar(datos)
    session["usuario_id"] = usuario_id

    return redirect(url_for("exito"))

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    # Buscamos al usuario por correo
    usuario = Usuario.obtener_por_email(email)

    if not usuario:
        flash("Correo o contraseña incorrectos.", "login")
        return redirect(url_for("inicio"))

    # Verificamos la clave encriptada
    if not bcrypt.check_password_hash(usuario.password, password):
        flash("Correo o contraseña incorrectos.", "login")
        return redirect(url_for("inicio"))

    # Guardamos el id en sesion
    session["usuario_id"] = usuario.id
    return redirect(url_for("exito"))

@app.route("/exito")
def exito():
    # Validar que el usuario tenga la sesion activa
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    usuario = Usuario.obtener_por_id(session["usuario_id"])
    if not usuario:
        session.clear()
        return redirect(url_for("inicio"))

    return render_template("exito.html", usuario=usuario)

@app.route("/logout")
def logout():
    # Borrar la sesion
    session.clear()
    return redirect(url_for("inicio"))