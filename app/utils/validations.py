from app import db
from .exceptions import *

class Validations():
    @staticmethod
    def check_if_exists(obj, type_obj):
        """
        Verifica si un objeto existe.

        Args:
            obj (object): El objeto a verificar, con todos sus atributos.
            type_obj (str): El nombre o tipo del objeto, utilizado en el mensaje de error.

        Returns:
            object: Retorna el objeto si existe.

        Raises:
            ValueError: Si el objeto no existe, lanza un error con el mensaje "{type_obj} not found".
        """
        if not obj:
            raise NotFoundError(f'{type_obj} not found')
        return obj

    @staticmethod
    def check_field_existence(attribute, value, name):
        """
        Verifica si un valor ya existe en un campo específico de la base de datos.

        Args:
            attribute (Column): La columna en la base de datos que se va a verificar.
            value (any): El valor que se espera encontrar en el atributo.
            name (str): El nombre descriptivo del campo para usar en el mensaje de error.

        Returns:
            bool: Retorna True si el valor ya existe en la base de datos.

        Raises:
            ValueError: Si el valor ya existe, lanza un error con el mensaje "{name} already exists".
        """
        if db.session.query(db.exists().where(attribute == value)).scalar():
            raise DuplicateValueError(f'{name} already exists. Please choose a different one.')

    @staticmethod
    def check_fk_existence(attribute, value, tablename):
        """
        Verifica la existencia de una clave foránea (foreign key) en una tabla.

        Args:
            attribute (Column): La columna en la base de datos que representa la clave foránea.
            value (any): El valor esperado de la clave foránea.
            tablename (str): El nombre de la tabla donde se busca la clave foránea.

        Returns:
            bool: Retorna True si la clave foránea existe en la tabla.

        Raises:
            ValueError: Si la clave foránea no existe, lanza un error con el mensaje
                        "The primary key {value} does not exist in the {tablename} table."
        """
        if not db.session.query(db.exists().where(attribute == value)).scalar():
            raise NotFoundError(f'The primary key {value} does not exist in the {tablename} table.')

    @staticmethod
    def check_data_pair_existence(attribute1, value1, attribute2, value2, name):
        """
        Verifica si una combinación de dos valores ya existe en la base de datos.

        Args:
            attribute1 (Column): La primera columna a verificar.
            value1 (any): El valor esperado de la primera columna.
            attribute2 (Column): La segunda columna a verificar.
            value2 (any): El valor esperado de la segunda columna.
            name (str): Nombre descriptivo de la combinación para usar en el mensaje de error.

        Returns:
            None

        Raises:
            ValueError: Si la combinación de valores ya existe, lanza un error con el mensaje
                        "{name} already exists. Please choose a different {name}."
        """
        if db.session.query(db.exists().where(db.and_(attribute1 == value1, attribute2 == value2))).scalar():
            raise DuplicateValueError(f'This {name} already exists. Please choose a different {name}.')
        
    @staticmethod
    def Check_data_time_of_day(data):
        options=['mañana','tarde','noche']
        if data not in options:
            raise InvalidDataError('The value entered in the time_of_day field is incorrect. It must be [mañana, tarde, noche].')
