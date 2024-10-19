from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource, fields, marshal
from app.services.user_service import UserService

# Crear un espacio de nombres (namespace) para los usuarios
user_ns = Namespace('users', description='Operaciones relacionadas con los usuarios')

# Modelo de entrada de usuario
entry_user_model = user_ns.model('User', {
    'first_name': fields.String(required=True, description='Nombre de usuario'),
    'last_name': fields.String(required=True, description='Apellido de usuario'),
    'nickname': fields.String(required=True, description='Apodo de usuario'),
    'email': fields.String(required=True, description='Email de usuario'),
    'user_password': fields.String(required=True, description='Contraseña'),
})

# Modelo de salida de usuario en el metodo get
get_user_response_model = user_ns.model('GetResponse', {
    'user_id': fields.Integer(description='ID de usuario'),
    'first_name': fields.String(description='Nombre de usuario'),
    'last_name': fields.String(description='Apellido de usuario'),
    'nickname': fields.String(description='Apodo de usuario'),
    'email': fields.String(description='Email de usuario'),
    'user_status': fields.Boolean(description='Estado del usuario (activo o inactivo)'),
    'user_created_date': fields.DateTime(description='Fecha y hora de creación del usuario')
})

# Definir el controlador de usuarios con decoradores para la documentación
@user_ns.route('/')
class UserResource(Resource):
    @user_ns.doc('get_all_users')
    def get(self):
        """
        Obtener todos los usuarios con sus datos
        ---
        Este método permite obtener una lista de todos los usuarios registrados en la base de datos.

        Responses:
        - 200: Retorna todos los datos de todos los usuarios.
        """
        # Llama al servicio para obtener todos los usuarios
        users = UserService.get_all_users()  
        # Usamos marshal para garantizar que la lista de usuarios se retorne conforme al modelo get_user_response_model.
        return marshal(users, get_user_response_model), 200 # Retorna todos los datos de los usuarios    
    
    @user_ns.doc('create_user')
    @user_ns.expect(entry_user_model, validate=True)  # Decorador para esperar el modelo en la petición
    def post(self):
        """
        Crear un nuevo usuario
        ---
        Este método permite crear un nuevo usuario proporcionando los siguientes datos:
        - Nombre.
        - Apellido.
        - Apodo.
        - Email.
        - Contraseña.

        Body Parameters:
        - first_name: Nombre del usuario a crear. 
        - last_name: Apellido del usuario.
        - nickname: Apodo del usuario.
        - email: Correo electronico del usuario.
        - user_password: Contraseña del usuario.

        Responses:
        - 201: Usuario creado con éxito.
        - 422: Si el nickname o el email ya existen.
        """
        # Obtiene los datos en formato JSON del cuerpo de la solicitud
        data = request.get_json()
        try:
            # Se llama al metodo create_user de la clase UserService para crear un nuevo objeto User y se guarda en la variable user
            user = UserService.create_user(data['first_name'], data['last_name'], data['nickname'], data['email'], data['user_password'])
            # Se fabrica la respuesta con su respectivo código de respuesta
            return make_response(jsonify([
                {'message': 'User created successfully'}, 
                {
                    'user': f'{user.first_name} {user.last_name}',
                    'nickname': user.nickname,
                    'email': user.email
                }]), 201)
        except ValueError as e:
            # Si el nickname o el email ya existen se responde un mensaje de error con el codigo 422
            return make_response(jsonify({'message': str(e)}), 422)   

@user_ns.route('/<int:user_id>')
@user_ns.param('user_id', 'ID del usuario')
class UserDetailResource(Resource):
    @user_ns.doc('get_user_by_user_id')
    def get(self, user_id):
        """
        Obtener datos de usuario
        ---
        Este método permite obtener todos los datos de un usuario basado en su ID.

        Responses:
        - 200: Retorna un JSON con todos los datos del usuario.
        - 404: Si el usuario no es encontrado.
        """
        try:
            # Llama al servicio para obtener el usuario asociado al ID
            user = UserService.get_user_by_user_id(user_id)            
            # Si el usuario se encuentra, aplicamos manualmente marshal para formatear la respuesta
            return marshal(user, get_user_response_model), 200
        except ValueError as e:
            # Si el usuario no es encontrado, devolvemos un mensaje de error con el código 404
            return make_response(jsonify({'message': str(e)}), 404)

    @user_ns.doc('delete_user')
    def delete(self, user_id):
        """
        Eliminar un usuario
        ---
        Este método permite eliminar un usuario existente basado en el ID del usuario.

        Path Parameters:
        - user_id: El ID del usuario a eliminar.

        Responses:
        - 200: Usuario eliminado con éxito.
        - 404: Si el usuario no se encuentra.
        """
        try:
            # Llama al servicio para eliminar al usuario
            UserService.delete_user(user_id)  
            # Usamos jsonify para enviar un mensaje de éxito en formato JSON.
            return make_response(jsonify({'message': 'User deleted successfully'}), 200)
        except ValueError as e:
            # Si el usuario no es encontrado, devolvemos un mensaje de error con el código 404
            return make_response(jsonify({'message': str(e)}), 404)

    @user_ns.doc('update_user')
    @user_ns.expect(entry_user_model, validate=False)
    def put(self, user_id):
        """
        Actualizar un usuario
        ---
        Este método permite actualizar la información de un usuario basado en el ID del usuario.

        Path Parameters:
        - user_id: El ID del usuario que se actualizará.

        Body Parameters:
        - first_name: Nuevo nombre del usuario (opcional).
        - last_name: Nuevo apellido del usuario (opcional).
        - nickname: El nuevo apodo de usuario (opcional).
        - email: El nuevo Email del usuario (opcional).
        - user_password: La nueva contraseña (opcional).

        Responses:
        - 200: Usuario actualizado con éxito.
        - 404: Si el usuario no se encuentra.
        """
        # Obtiene los nuevos datos para la actualización
        new_data = request.get_json()  
        try:
            # Llama al servicio para actualizar el usuario
            UserService.update_user(user_id, new_data)  
            # Usamos jsonify para enviar un mensaje de éxito en formato JSON.
            return make_response(jsonify({'message': 'User updated successfully'}), 200)
        except ValueError as e:
            # Si el usuario no es encontrado, devolvemos un mensaje de error con el código 404
            return make_response(jsonify({'message': str(e)}), 404)     

