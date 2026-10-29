# CinePedia: Plataforma de Gestión de Películas y Comentarios

## Sobre el Proyecto
CinePedia es una aplicación web diseñada para amantes del cine, donde los usuarios pueden compartir sus películas favoritas, consultar estrenos y debatir a través de comentarios en comunidad.

Este proyecto fue desarrollado íntegramente por mí como parte de mi examen de certificación Fullstack, poniendo énfasis en buenas prácticas de programación, seguridad de datos, diseño limpio y una arquitectura escalable.

---

## Tecnologías y Arquitectura
El sistema está construido bajo el patrón de diseño MVC (Modelo-Vista-Controlador), lo que garantiza un código ordenado, separado y mantenible.

- **Backend:** Python con Flask.
- **Base de Datos:** MySQL con relaciones de uno a muchos (1:N) entre usuarios, películas y comentarios.
- **Seguridad:** Encriptación de contraseñas con Bcrypt, gestión de claves mediante variables de entorno (`.env`) y manejo seguro de sesiones con `SECRET_KEY`.
- **Frontend:** Plantillas HTML5 interactivas con Jinja2 y estilos en CSS puro personalizados en tonos rosa suave.

---

## Funcionalidades Clave

### 1. Seguridad y Usuarios
Más allá de un registro simple, el sistema cuenta con validaciones estrictas para asegurar que los correos sean únicos y las contraseñas seguras. Protegemos las rutas para que solo usuarios autenticados puedan acceder a la plataforma y gestionar contenido.

### 2. Gestión Inteligente de Películas
Los usuarios pueden registrar, visualizar, editar y eliminar películas de la plataforma.
- **Protección de Propiedad:** Implementé una lógica de backend que asegura que solo el creador de una película pueda editarla o eliminarla, previniendo accesos no autorizados mediante manipulación de URLs.
- **Validaciones de Negocio:** El sistema valida que el título de la película sea único en la base de datos, exige campos completos y mantiene la información de la sinopsis en el formulario si existen errores de validación.

### 3. Sistema de Comentarios en Comunidad
Permite interacción activa entre los usuarios para debatir sobre cada filme.
- El sistema impide que el usuario creador de la película pueda comentar en su propia publicación.
- Los comentarios se despliegan automáticamente en orden cronológico inverso (del más reciente al más antiguo).
- Solo el autor original de un comentario tiene permitido eliminarlo.

---

## Autor
**Elisa Soto**  
Desarrolladora Fullstack Python
contacto: elisasoto@liceovvh.cl