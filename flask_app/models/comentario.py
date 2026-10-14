from flask_app.config.mysqlconnection import conectar_mysql

class Comentario:
    def __init__(self, datos):
        # Mapeo de campos de comentarios
        self.id = datos['id']
        self.contenido = datos['contenido']
        self.usuario_id = datos['usuario_id']
        self.pelicula_id = datos['pelicula_id']
        self.created_at = datos['created_at']
        self.updated_at = datos['updated_at']
        # Nombre del usuario autor del comentario
        self.autor = datos.get('autor', '')

    @classmethod
    def guardar(cls, datos):
        # Crear un nuevo comentario
        query = """
            INSERT INTO comentarios (contenido, usuario_id, pelicula_id)
            VALUES (%(contenido)s, %(usuario_id)s, %(pelicula_id)s);
        """
        return conectar_mysql().consultar_bd(query, datos)

    @classmethod
    def obtener_por_pelicula(cls, pelicula_id):
        # Traer comentarios ordenados del mas reciente al mas antiguo
        query = """
            SELECT comentarios.*, usuarios.nombre AS autor 
            FROM comentarios 
            JOIN usuarios ON comentarios.usuario_id = usuarios.id 
            WHERE comentarios.pelicula_id = %(pelicula_id)s 
            ORDER BY comentarios.created_at DESC;
        """
        resultados = conectar_mysql().consultar_bd(query, {"pelicula_id": pelicula_id})
        lista = []
        if resultados:
            for fila in resultados:
                lista.append(cls(fila))
        return lista

    @classmethod
    def obtener_por_id(cls, comentario_id):
        # Buscar un comentario especifico
        query = "SELECT * FROM comentarios WHERE id = %(id)s;"
        resultados = conectar_mysql().consultar_bd(query, {"id": comentario_id})
        if not resultados:
            return False
        return cls(resultados[0])

    @classmethod
    def eliminar(cls, comentario_id):
        # Borrar comentario de la base de datos
        query = "DELETE FROM comentarios WHERE id = %(id)s;"
        return conectar_mysql().consultar_bd(query, {"id": comentario_id})