import re
from datetime import datetime, date
from flask import flash
from flask_app.config.mysqlconnection import conectar_mysql

# Expresiones regulares para validar correo, letras y contraseñas
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
SOLO_LETRAS = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$')
PASS_MAYUSCULA = re.compile(r'[A-Z]')
PASS_NUMERO = re.compile(r'[0-9]')

class Usuario:
    def __init__(self, datos):
        self.id = datos['id']
        self.nombre = datos['nombre']
        self.apellido = datos['apellido']
        self.email = datos['email']
        self.password = datos['password']
        self.created_at = datos['created_at']
        self.updated_at = datos['updated_at']

    @classmethod
    def guardar(cls, datos):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return conectar_mysql("").consultar_bd(query, datos)

    @classmethod
    def obtener_por_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        datos = {"email": email}
        resultados = conectar_mysql("CinePedia_db").consultar_bd(query, datos)

        if len(resultados) < 1:
            return False
        return cls(resultados[0])

    @classmethod
    def obtener_por_id(cls, usuario_id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        datos = {"id": usuario_id}
        resultados = conectar_mysql("CinePedia_db").consultar_bd(query, datos)

        if len(resultados) < 1:
            return False
        return cls(resultados[0])

    @staticmethod
    def validar_registro(form):
        es_valido = True

        # Validacion del nombre
        nombre = form.get("nombre", "").strip()
        if len(nombre) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            es_valido = False
        elif not SOLO_LETRAS.match(nombre):
            flash("El nombre solo debe contener letras.", "registro")
            es_valido = False

        # Validacion del apellido
        apellido = form.get("apellido", "").strip()
        if len(apellido) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            es_valido = False
        elif not SOLO_LETRAS.match(apellido):
            flash("El apellido solo debe contener letras.", "registro")
            es_valido = False

        # Validacion del email
        email = form.get("email", "").strip()
        if not EMAIL_REGEX.match(email):
            flash("Ingrese un correo electronico valido.", "registro")
            es_valido = False
        else:
            # Revisar que no este duplicado en la base de datos
            usuario_existente = Usuario.obtener_por_email(email)
            if usuario_existente:
                flash("Este correo ya esta registrado.", "registro")
                es_valido = False

        # Validacion de contraseña
        password = form.get("password", "")
        confirm = form.get("confirm_password", "")

        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "registro")
            es_valido = False
        if not PASS_MAYUSCULA.search(password):
            flash("La contraseña debe incluir al menos una letra mayúscula.", "registro")
            es_valido = False
        if not PASS_NUMERO.search(password):
            flash("La contraseña debe incluir al menos un número.", "registro")
            es_valido = False
        if password != confirm:
            flash("Las contraseñas no coinciden.", "registro")
            es_valido = False

        return es_valido