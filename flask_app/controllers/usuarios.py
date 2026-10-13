from flask import render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.usuario import Usuario

bcrypt = Bcrypt(app)

@app.route("/")
def inicio():
    if "usuario_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("inicio.html")

@app.route("/registrar", methods=["POST"])
def registrar():
    if not Usuario.validar_registro(request.form):
        return redirect(url_for("inicio"))

    pass_hash = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

    datos = {
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip().lower(),
        "password": pass_hash
    }

    usuario_id = Usuario.guardar(datos)
    session["usuario_id"] = usuario_id
    session["nombre"] = datos["nombre"]

    return redirect(url_for("dashboard"))

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    usuario = Usuario.obtener_por_email(email)

    if not usuario or not bcrypt.check_password_hash(usuario.password, password):
        flash("Credenciales incorrectas.", "login")
        return redirect(url_for("inicio"))

    session["usuario_id"] = usuario.id
    session["nombre"] = usuario.nombre

    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))