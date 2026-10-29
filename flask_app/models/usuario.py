import re
from flask import flash
from flask_app.config.mysqlconnection import conectar_mysql

# Expresion regular para validar el formato de e-mail
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    def __init__(self, datos):
        # Mapeo de columnas de la tabla usuarios
        self.id = datos['id']
        self.nombre = datos['nombre']
        self.apellido = datos['apellido']
        self.email = datos['email']
        self.password = datos['password']
        self.created_at = datos['created_at']
        self.updated_at = datos['updated_at']

    @classmethod
    def guardar(cls, datos):
        # Insertar un nuevo usuario en la base de datos
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return conectar_mysql().consultar_bd(query, datos)

    @classmethod
    def obtener_por_email(cls, email):
        # Buscar usuario por correo para login y validaciones
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultados = conectar_mysql().consultar_bd(query, {"email": email})
        if not resultados:
            return False
        return cls(resultados[0])

    @classmethod
    def obtener_por_id(cls, usuario_id):
        # Obtener datos del usuario en sesion mediante su id
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultados = conectar_mysql().consultar_bd(query, {"id": usuario_id})
        if not resultados:
            return False
        return cls(resultados[0])

    @staticmethod
    def validar_registro(form):
        # Validar los datos ingresados en el formulario de registro
        es_valido = True

        # Validar nombre
        nombre = form.get("nombre", "").strip()
        if len(nombre) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            es_valido = False

        # Validar apellido
        apellido = form.get("apellido", "").strip()
        if len(apellido) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            es_valido = False

        # Validar correo
        email = form.get("email", "").strip().lower()
        if not EMAIL_REGEX.match(email):
            flash("Ingrese un e-mail con formato valido.", "registro")
            es_valido = False
        elif Usuario.obtener_por_email(email):
            flash("El e-mail ya se encuentra registrado.", "registro")
            es_valido = False

        # Validar contraseñas
        password = form.get("password", "")
        confirm = form.get("confirm_password", "")

        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "registro")
            es_valido = False
        if password != confirm:
            flash("Las contraseñas no coinciden.", "registro")
            es_valido = False

        return es_valido