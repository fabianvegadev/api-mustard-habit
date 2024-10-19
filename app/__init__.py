from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_migrate import Migrate
from app.config import Config

# Inicializamos las extensiones globalmente para luego asociarlas a la app en la función create_app
db = SQLAlchemy()  # Para la interacción con la base de datos usando SQLAlchemy
migrate = Migrate()  # Para gestionar las migraciones de la base de datos
bcrypt = Bcrypt()  # Para el hash y verificación de contraseñas de los usuarios
jwt = JWTManager()  # Para la gestión de tokens JWT en la autenticación

def create_app():
    """Función factory para crear la aplicación Flask y configurar sus componentes."""
    
    # Creamos una instancia de la aplicación Flask
    app = Flask(__name__)
    
    # Cargamos la configuración de la aplicación desde el archivo de configuración
    app.config.from_object(Config)

    # Inicializamos las extensiones con la aplicación
    db.init_app(app)  # Inicializar SQLAlchemy con la app
    bcrypt.init_app(app)  # Inicializar Bcrypt con la app
    jwt.init_app(app)  # Inicializar JWTManager con la app
    migrate.init_app(app, db)  # Inicializar Migrate con la app y la base de datos

    # Autorizador JWT para integrar con la documentación Swagger
    authorizations = {
        'Bearer': {
            'type': 'apiKey',  # Tipo apiKey define que el token JWT se envía en el encabezado de la solicitud
            'in': 'header',  # El token JWT se debe enviar en el encabezado de la solicitud HTTP
            'name': 'Authorization',  # Nombre del campo del encabezado HTTP para el token
            'description': 'JWT Bearer token. Ejemplo: "Bearer {token}"'  # Instrucción sobre cómo enviar el token
        }
    }

    # Configuramos la API Flask-RESTX, que nos ayuda a crear endpoints RESTful con documentación Swagger integrada
    api = Api(
        app,  # La aplicación Flask en la que registramos la API
        title='API de Usuarios y Hábitos',  # Título para la documentación Swagger
        version='1.0',  # Versión de la API
        description='API para gestión de hábitos, usuarios, asignaciones y logros ',  # Descripción de la API
        authorizations=authorizations,  # Añadimos la configuración de JWT a la API
        security='Bearer'  # Define que los endpoints por defecto usan el esquema de seguridad JWT
    )

    # Importamos los controladores y namespaces que organizan las rutas/endpoints de la API
    from .controllers.user_controller import user_ns  # Controlador para la gestión de usuarios
    from .controllers.habit_controller import habit_ns # Controlador para la gestión de hábitos
    from .controllers.assignment_controller import assignment_ns # Controlador para la gestión de asignaciones de hábitos por cada usuario
    from .controllers.completed_date_controller import completed_date_ns # Controlador para la gestión de fechas en que se completan los hábitos

    # Registramos cada namespace (grupo de rutas) en la API
    api.add_namespace(user_ns, path='/users')  # Registrar el namespace de usuarios en /users
    api.add_namespace(habit_ns, path='/habits') # Registrar el namespace de hábitos en /habits
    api.add_namespace(assignment_ns, path='/assignments') # Registrar el namespace de asignaciones de hábitos por cada usuario en /assignment
    api.add_namespace(completed_date_ns, path='/completed_dates') # Registrar el namespace de fechas en que se completan los hábitos en /completed_dates

    # Retornamos la aplicación ya configurada
    return app
