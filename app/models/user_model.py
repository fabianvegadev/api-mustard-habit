from app import db
from datetime import datetime


class User(db.Model):
    """
    Modelo que representa un usuario en el sistema.

    Cada usuario tiene un nombre de usuario, apellido, apodo, correo electrónico, contraseña encriptada y un estado que indica si el usuario está activo. También se registra la fecha de creación del usuario.

    Atributos:
        user_id (int): Identificador único del usuario (clave primaria).
        first_name (str): Nombre del usuario.
        last_name (str): Apellido del usuario.
        nickname (str): Apodo de usuario, debe ser único.
        email (str): Correo electrónico del usuario, debe ser único.
        user_password (str): Contraseña encriptada del usuario.
        user_status (bool): Estado del usuario, indica si está activo o inactivo (True = activo, False = inactivo).
        user_created_date (datetime): Fecha de creación del usuario.
    """

    __tablename__ = 'users'  # Especifica el nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    user_id = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    first_name = db.Column(db.String(100), nullable=False)  # Nombre del usuario, no puede ser nulo
    last_name = db.Column(db.String(100), nullable=False)  # Apellido del usuario, no puede ser nulo
    nickname = db.Column(db.String(100), unique=True, nullable=False)  # Apodo de usuario, debe ser único y no nulo
    email = db.Column(db.String(100), unique=True, nullable=False)  # Correo electrónico del usuario, debe ser único y no nulo
    user_password = db.Column(db.String(200), nullable=False)  # Contraseña encriptada del usuario, no puede ser nula
    user_status = db.Column(db.Boolean, default=True, nullable=False)  # Estado del usuario, por defecto es activo
    user_created_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)  # Fecha de creación del usuario, no puede ser nula
    assignments = db.relationship('Assignment', backref='user', lazy=True) # Relación con la tabla assignments

    def __init__(self, first_name, last_name, nickname, email, user_password):
        """
        Constructor de la clase User.

        Args:
            first_name (str): El nombre del usuario.
            last_name (str): El apellido del usuario.
            nickname (str): El apodo de usuario, debe ser único.
            email (str): El correo electrónico del usuario, debe ser único.
            user_password (str): La contraseña encriptada del usuario.
            user_status (bool): El estado del usuario (activo/inactivo).
            user_created_date (datetime): La fecha de creación del usuario.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname
        self.email = email
        self.user_password = user_password