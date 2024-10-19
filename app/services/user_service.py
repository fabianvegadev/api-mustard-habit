from app import db, bcrypt
from app.models.user_model import User
from app.utils.validations import Validations

class UserService:
    """
    Servicio para gestionar las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    relacionadas con los usuarios en la base de datos.
    """
    
    @staticmethod
    def create_user(first_name, last_name, nickname, email, user_password):
        """
        Crea un nuevo usuario en el sistema.

        Args:
            first_name (str): El nombre del usuario.
            last_name (str): El apellido del usuario.
            nickname (str): El apodo del nuevo usuario.
            email (str): El correo electrónico del nuevo usuario.
            user_password (str): La contraseña en texto plano que será encriptada.

        Returns:
            User: El usuario recién creado.

        Raises:
            ValueError: Si el 'nickname' o el 'email' ya existen en la base de datos.
        """
        # Verificando si el nickname ya existe
        Validations.check_field_existence(User.nickname, nickname, 'Nickname')
        # Verificando si el email ya existe
        Validations.check_field_existence(User.email, email, 'Email')
        # Generando un hash seguro de la contraseña con bcrypt
        hashed_password = bcrypt.generate_password_hash(user_password).decode('utf-8')
        # Crear un nuevo usuario con la contraseña hasheada y los demás datos proporcionados
        user = User(first_name, last_name, nickname, email, user_password=hashed_password)
        # Añadir el nuevo usuario a la base de datos
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_all_users():
        """
        Obtiene todos los usuarios registrados en la base de datos.

        Returns:
            List[User]: Una lista con todos los usuarios registrados.
        """
        # Retorna todos los registros de la tabla User
        return User.query.all()

    @staticmethod
    def get_user_by_user_id(user_id):
        """
        Obtiene un usuario por su ID de usuario.

        Args:
            user_id (int): El ID del usuario que se desea obtener.

        Returns:
            User: El usuario que coincide con el ID proporcionado.

        Raises:
            ValueError: Si el usuario no existe.
        """
        # Buscar al usuario por su ID
        user = User.query.filter_by(user_id=user_id).first()
        # Validar si el usuario existe
        user_validated = Validations.check_if_exists(user, 'User')
        return user_validated

    @staticmethod
    def update_user(user_id, new_data):
        """
        Actualiza los datos de un usuario existente.

        Args:
            user_id (int): El ID del usuario a actualizar.
            new_data (dict): Un diccionario con los nuevos datos del usuario. 
                            Puede incluir 'first_name', 'last_name', 'nickname', 'email' o 'user_password'.

        Returns:
            None

        Raises:
            ValueError: Si el 'nickname' o 'email' proporcionados ya existen en la base de datos.
        """
        # Buscar al usuario por su ID
        user = UserService.get_user_by_user_id(user_id)
        # Actualizar los datos según lo que se proporcione en 'new_data'
        if 'first_name' in new_data:
            user.first_name = new_data['first_name']
        if 'last_name' in new_data:
            user.last_name = new_data['last_name']
        if 'nickname' in new_data:
            Validations.check_field_existence(User.nickname, new_data['nickname'], 'Nickname')
            user.nickname = new_data['nickname']
        if 'email' in new_data:
            Validations.check_field_existence(User.email, new_data['email'], 'Email')
            user.email = new_data['email']
        if 'user_password' in new_data:
            user.user_password = bcrypt.generate_password_hash(new_data['user_password']).decode('utf-8')
        # Guardar los cambios en la base de datos
        db.session.commit()

    @staticmethod
    def delete_user(user_id):
        """
        Elimina un usuario de la base de datos.

        Args:
            user_id (int): El ID del usuario a eliminar.

        Returns:
            None
        """
        # Buscar al usuario por su ID
        user = UserService.get_user_by_user_id(user_id)
        # Eliminar el usuario de la base de datos
        db.session.delete(user)
        db.session.commit()
