from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource, fields, marshal
from app.services.habit_service import HabitService
from app.utils.exceptions import *

# Crear un espacio de nombres (namespace) para los hábitos
habit_ns = Namespace('habits', description='Operaciones relacionadas con los hábitos')

# Modelo de entrada para la creación de un nuevo hábito
entry_habit_model = habit_ns.model('Habit', {
    'habit_name': fields.String(required=True, description='Nombre del hábito'),
    'time_of_day': fields.String(required=True, description='Momento del día (mañana, tarde, noche)', enum=['mañana', 'tarde', 'noche']),
})

# Modelo de salida para la respuesta de las operaciones relacionadas con los hábitos
get_habit_response_model = habit_ns.model('HabitResponse', {
    'habit_id': fields.Integer(description='ID del hábito'),
    'habit_name': fields.String(description='Nombre del hábito'),
    'time_of_day': fields.String(description='Momento del día (mañana, tarde, noche)'),
    'habit_status': fields.Boolean(description='Estado del hábito (activo o inactivo)'),
})

# Definir el controlador de hábitos con decoradores para la documentación
@habit_ns.route('/')
class HabitResource(Resource):

    @habit_ns.doc('get_all_habits')
    def get(self):
        """
        Obtener todos los hábitos con sus datos
        ---
        Este método permite obtener una lista de todos los hábitos registrados.

        Responses:
        - 200: Retorna una lista de todos los hábitos con sus datos.
        """
        habits = HabitService.get_all_habits()  # Llama al servicio para obtener todos los hábitos
        return marshal(habits, get_habit_response_model), 200 # Retorna todos los hábitos en el formato estipulado

    @habit_ns.doc('create_habit')
    @habit_ns.expect(entry_habit_model, validate=True)  # Decorador para esperar el modelo en la petición
    def post(self):
        """
        Crear un nuevo hábito
        ---
        Este método permite crear un nuevo hábito proporcionando los siguientes datos:
        - Nombre del hábito.
        - Momento del día.

        Body Parameters:
        - habit_name: Nombre del hábito a crear.
        - time_of_day: Momento del día (mañana, tarde, noche).

        Responses:
        - 201: Hábito creado con éxito.
        - 400: Si ocurre un error debido a un valor inválido (error por defecto).
        - 422: si el hábito ya existe
        """
        # Obtiene los datos en formato JSON del cuerpo de la solicitud
        data = request.get_json()
        try:
            # Crear el nuevo hábito
            new_habit = HabitService.create_habit(data['habit_name'], data['time_of_day'])  
            # Retornar el nuevo hábito creado
            return make_response(jsonify([
                {'message': 'Habit created successfully'}, 
                {
                    'habit_name': new_habit.habit_name,
                    'time_of_day': new_habit.time_of_day
                }]), 201) 
        except DuplicateValueError as e:
            return make_response(jsonify({'message': str(e)}), 422)  
        except InvalidDataError as e:
            return make_response(jsonify({'message': str(e)}), 422) 
        

@habit_ns.route('/<int:habit_id>')
@habit_ns.param('habit_id', 'ID del hábito')
class HabitDetailResource(Resource):

    @habit_ns.doc('get_habit_by_id')
    def get(self, habit_id):
        """
        Obtener un hábito por su ID
        ---
        Este método permite obtener todos los datos de un hábito basado en su ID.

        Responses:
        - 200: Retorna un JSON con todos los datos del hábito.
        - 404: Si el hábito no es encontrado.
        """
        try:
            # Llama al servicio para obtener el hábito asociado al ID
            habit = HabitService.get_habit_by_id(habit_id)
            # Retorna todos los datos del hábito en el formato estipulado
            return marshal(habit, get_habit_response_model), 200
        except NotFoundError as e:
            return make_response(jsonify({'message': str(e)}), 404) 

    @habit_ns.doc('update_habit')
    @habit_ns.expect(entry_habit_model, validate=False)  # Decorador para esperar el modelo en la petición
    def put(self, habit_id):
        """
        Actualizar un hábito existente
        ---
        Este método permite actualizar la información de un hábito basado en el ID del hábito.

        Path Parameters:
        - habit_id: El ID del hábito que se actualizará.

        Body Parameters:
        - habit_name: Nuevo nombre del hábito (opcional).
        - time_of_day: Nuevo momento del día (opcional).

        Responses:
        - 200: Hábito actualizado con éxito.
        - 404: Si el hábito no se encuentra.
        """
        # Obtiene los nuevos datos para la actualización
        new_data = request.get_json()  
        try:
            # Actualizar el hábito con los nuevos datos
            HabitService.update_habit(habit_id, new_data['habit_name'], new_data['time_of_day'])  
            # Usamos jsonify para enviar un mensaje de éxito en formato JSON.
            return make_response(jsonify({'message': 'Habit updated successfully'}), 200)
        except InvalidDataError as e:
            return make_response(jsonify({'message': str(e)}), 422) 
        except NotFoundError as e:
            # Si el hábito no es encontrado, devolvemos un mensaje de error con el código 404
            return make_response(jsonify({'message': str(e)}), 404)  

    @habit_ns.doc('delete_habit')
    def delete(self, habit_id):
        """
        Eliminar un hábito
        ---
        Este método permite eliminar un hábito existente basado en el ID del hábito.

        Path Parameters:
        - habit_id: El ID del hábito a eliminar.

        Responses:
        - 200: Hábito eliminado con éxito.
        - 404: Si el hábito no se encuentra.
        """
        try:
            # Llama al servicio para eliminar el hábito
            HabitService.delete_habit(habit_id)  
            return make_response(jsonify({'message': 'Habit deleted successfully'}), 200)
        except NotFoundError as e:
            # Si el hábito no es encontrado, devolvemos un mensaje de error con el código 404
            return make_response(jsonify({'message': str(e)}), 404) 
