from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource, fields, marshal
from app.services.completed_date_service import CompletedDateService

# Definición del namespace para las operaciones relacionadas con las fechas completadas de los hábitos.
completed_date_ns = Namespace('completed_dates', description='Operaciones relacionadas con las fechas en que se completan los hábitos asignados')

# Modelo de entrada para la creación de una fecha de completación.
entry_completed_date_model = completed_date_ns.model('CompletedDates', {
    'completed_date': fields.Date(description='Fecha en que se completa el hábito'),
    'fk_assignment_id': fields.Integer(required=True, description='ID de la asignacion del hábito a un usuario')
})

# Modelo de respuesta para obtener una fecha de completación.
get_completed_date_response_model = completed_date_ns.model('CompletedDateResponse', {
    'completed_date_id': fields.Integer(description='ID de la fecha en que se completó un hábito'),
    'completed_date': fields.Date(description='Fecha en que se completó un hábito asignado'),
    'fk_assignment_id': fields.Integer(description='ID de la asignación del hábito a un usuario')
})

@completed_date_ns.route('/')
class CompletedDateResource(Resource):
    """
    Recurso para manejar operaciones de fechas completadas de hábitos.
    """

    @completed_date_ns.doc('get_all_dates')
    def get(self):
        """
        Obtener todas las fechas completadas registradas.
        ---
        Este método recupera todas las fechas en que se completaron hábitos asignados en la base de datos.
        
        Returns:
            Response: JSON con la lista de fechas completadas y el código de estado 200.
        """
        dates = CompletedDateService.get_all_dates()
        return marshal(dates, get_completed_date_response_model), 200

    @completed_date_ns.doc('create_completed_date')
    @completed_date_ns.expect(entry_completed_date_model, validate=True)
    def post(self):
        """
        Crear una nueva fecha de completación de hábito.
        ---
        Este método permite crear una nueva fecha asociada a la asignación de un hábito.

        Returns:
            Response: Mensaje de éxito con el código de estado 201 si se crea correctamente.
            Response: Mensaje de error con el código de estado 422 si ya existe la fecha o si hay algún problema.
        """
        data = request.get_json()
        try:
            new_completed_date = CompletedDateService.create_completed_date(data['fk_assignment_id'], data['completed_date'])
            return make_response(jsonify(
                {'message': 'Date created successfully', 'date': new_completed_date.completed_date}), 201)
        except ValueError as e:
            return make_response(jsonify({'message': str(e)}), 422)

@completed_date_ns.route('/<int:fk_assignment_id>')
@completed_date_ns.param('fk_assignment_id', 'ID de la asignación')
class CompletedDateAssignmentResource(Resource):
    """
    Recurso para manejar operaciones de fechas completadas por ID de asignación.
    """

    @completed_date_ns.doc('get_all_dates_by_assignment_id')
    def get(self, fk_assignment_id):
        """
        Obtener todas las fechas de completación por ID de asignación.
        ---
        Este método permite obtener todas las fechas en que se completó un hábito para una asignación específica.

        Args:
            fk_assignment_id (int): ID de la asignación a consultar.

        Returns:
            Response: Lista de fechas asociadas a la asignación y el código de estado 200.
            Response: Mensaje de error con el código de estado 404 si no existen fechas.
        """
        try:
            # Llama al servicio para obtener todas las fechas asociadas a la asignación específica.
            dates = CompletedDateService.get_all_dates_by_assignment_id(fk_assignment_id)
            # Si se encuentran las fechas, se formatea la respuesta con marshal.
            return marshal(dates, get_completed_date_response_model), 200
        except ValueError as e:
            # En caso de error, se retorna un mensaje con el código de error 422.
            return make_response(jsonify({'message': str(e)}), 404)
        
@completed_date_ns.route('/<int:completed_date_id>')
@completed_date_ns.param('completed_date_id', 'ID de la fecha')
class CompletedDateAssignmentResource(Resource):
    """
    Recurso para manejar operaciones de fechas completadas por ID de fecha de completación.
    """

    @completed_date_ns.doc('delete_date_by_date_id')
    def delete(self, completed_date_id):
        """
        Eliminar una fecha de completación por su ID.
        ---
        Este método permite eliminar una fecha en que se completó un hábito específico.

        Args:
            completed_date_id (int): ID de la fecha de completación a eliminar.

        Returns:
            Response: Mensaje de éxito con el código de estado 200 si se elimina la fecha correctamente.
            Response: Mensaje de error con el código de estado 404 si la fecha no existe.
        """
        try:
            # Llama al servicio para eliminar la fecha específica.
            CompletedDateService.delete_date(completed_date_id)
            return make_response(jsonify({'message': 'Date deleted successfully'}), 200)
        except ValueError as e:
            # En caso de error, se retorna un mensaje con el código de error 404.
            return make_response(jsonify({'message': str(e)}), 404)