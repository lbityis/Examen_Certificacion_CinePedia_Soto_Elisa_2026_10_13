from flask import render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.usuario import Usuario

# Inicializar objeto de encriptacion
bcrypt = Bcrypt(app)

@app.route("/")
def inicio():
    # Redirigir al dashboard si ya hay sesion
    if "usuario_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("inicio.html")

@app.route("/registrar", methods=["POST"])
def registrar():
    # Validar campos del formulario
    if not Usuario.validar_registro(request.form):
        return redirect(url_for("inicio"))

    # Hashear contraseña antes de guardar
    pass_hash = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

    datos = {
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip().lower(),
        "password": pass_hash
    }

    # Guardar en base de datos e iniciar sesion
    usuario_id = Usuario.guardar(datos)
    session["usuario_id"] = usuario_id
    session["nombre"] = datos["nombre"]

    return redirect(url_for("dashboard"))

@app.route("/login", methods=["POST"])
def login():
    # Procesar inicio de sesion
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    # Verificar existencia del usuario
    usuario = Usuario.obtener_por_email(email)

    if not usuario or not bcrypt.check_password_hash(usuario.password, password):
        flash("Credenciales incorrectas.", "login")
        return redirect(url_for("inicio"))

    # Guardar datos en sesion
    session["usuario_id"] = usuario.id
    session["nombre"] = usuario.nombre

    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    # Limpiar sesion y cerrar cuenta
    session.clear()
    return redirect(url_for("inicio"))