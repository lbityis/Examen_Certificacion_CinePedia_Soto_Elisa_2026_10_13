from flask import flash
from flask_app.config.mysqlconnection import conectar_mysql

class Pelicula:
    def __init__(self, datos):
        self.id = datos['id']
        self.titulo = datos['titulo']
        self.director = datos['director']
        self.fecha_estreno = datos['fecha_estreno']
        self.sinopsis = datos['sinopsis']
        self.usuario_id = datos['usuario_id']
        self.created_at = datos['created_at']
        self.updated_at = datos['updated_at']
        self.creador = datos.get('creador', '')

    @classmethod
    def guardar(cls, datos):
        query = """
            INSERT INTO peliculas (titulo, director, fecha_estreno, sinopsis, usuario_id)
            VALUES (%(titulo)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s);
        """
        return conectar_mysql().consultar_bd(query, datos)

    @classmethod
    def obtener_todas(cls):
        query = """
            SELECT peliculas.*, usuarios.nombre AS creador 
            FROM peliculas 
            JOIN usuarios ON peliculas.usuario_id = usuarios.id;
        """
        resultados = conectar_mysql().consultar_bd(query)
        lista = []
        if resultados:
            for fila in resultados:
                lista.append(cls(fila))
        return lista

    @classmethod
    def obtener_por_id(cls, pelicula_id):
        query = """
            SELECT peliculas.*, usuarios.nombre AS creador 
            FROM peliculas 
            JOIN usuarios ON peliculas.usuario_id = usuarios.id 
            WHERE peliculas.id = %(id)s;
        """
        resultados = conectar_mysql().consultar_bd(query, {"id": pelicula_id})
        if not resultados:
            return False
        return cls(resultados[0])

    @classmethod
    def obtener_por_titulo(cls, titulo):
        query = "SELECT * FROM peliculas WHERE titulo = %(titulo)s;"
        resultados = conectar_mysql().consultar_bd(query, {"titulo": titulo})
        if not resultados:
            return False
        return cls(resultados[0])

    @classmethod
    def actualizar(cls, datos):
        query = """
            UPDATE peliculas 
            SET titulo = %(titulo)s, director = %(director)s, 
                fecha_estreno = %(fecha_estreno)s, sinopsis = %(sinopsis)s 
            WHERE id = %(id)s;
        """
        return conectar_mysql().consultar_bd(query, datos)

    @classmethod
    def eliminar(cls, pelicula_id):
        query = "DELETE FROM peliculas WHERE id = %(id)s;"
        return conectar_mysql().consultar_bd(query, {"id": pelicula_id})

    @staticmethod
    def validar_pelicula(form, pelicula_id=None):
        es_valido = True

        titulo = form.get("titulo", "").strip()
        director = form.get("director", "").strip()
        fecha = form.get("fecha_estreno", "").strip()
        sinopsis = form.get("sinopsis", "").strip()

        if len(titulo) < 3:
            flash("El nombre de la película debe tener al menos 3 caracteres.", "pelicula")
            es_valido = False
        else:
            # Validacion BONUS: Titulo unico
            existente = Pelicula.obtener_por_titulo(titulo)
            if existente and (pelicula_id is None or str(existente.id) != str(pelicula_id)):
                flash("El nombre de la película debe ser único.", "pelicula")
                es_valido = False

        if len(director) < 3:
            flash("El director debe tener al menos 3 caracteres.", "pelicula")
            es_valido = False

        if not fecha:
            flash("La fecha de estreno no puede estar vacía.", "pelicula")
            es_valido = False

        if len(sinopsis) < 3:
            flash("La sinopsis no puede estar vacía y debe tener al menos 3 caracteres.", "pelicula")
            es_valido = False

        return es_valido