from flask_app import app

# Importación de controladores
from flask_app.controllers.usuarios import usuarios_bp
from flask_app.controllers.peliculas import peliculas_bp
from flask_app.controllers.comentarios import comentarios_bp

# Registro de BluePrints
app.register_blueprint(usuarios_bp)
app.register_blueprint(peliculas_bp)
app.register_blueprint(comentarios_bp)

if __name__ == "__main__":
    app.run(debug=True)