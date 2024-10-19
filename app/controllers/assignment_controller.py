from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource, fields, marshal
from app.services.assignment_service import AssignmentService

# Crear un espacio de nombres (namespace) para las asignaciones
assignment_ns = Namespace('assignments', description='Operaciones relacionadas a la asignación de hábitos por cada usuario')

# Modelo de entrada para la creación de asignaciones
entry_assignment_model = assignment_ns.model('Assignment', {
    'fk_user_id': fields.Integer(required=True, description='ID del usuario que asignó el hábito'),
    'fk_habit_id': fields.Integer(required=True, description='ID del hábito asignado')
})

# Modelo de respuesta para obtener información de asignaciones
get_assignment_response_model = assignment_ns.model('AssignmentResponse', {    
    'assignment_id': fields.Integer(description='ID de la asignación'),
    'created_date': fields.DateTime(description='Fecha de la asignación'),
    'assignment_status': fields.Boolean(description='Estado de la asignación (activado/desactivado)'),
    'fk_user_id': fields.Integer(description='ID del usuario que asignó el hábito'),
    'fk_habit_id': fields.Integer(description='ID del hábito asignado')
})

@assignment_ns.route('/')
class AssignmentResource(Resource):
    @assignment_ns.doc('create_assignment')
    @assignment_ns.expect(entry_assignment_model, validate=True) 
    def post(self):
        """
        Crear una nueva asignación.
        ---
        Este método permite crear una nueva asignación de un hábito a un usuario, proporcionando los IDs del usuario y del hábito.

        Body Parameters:
        - fk_user_id: ID del usuario que asigna el hábito.
        - fk_habit_id: ID del hábito que se asigna.

        Responses:
        - 201: Asignación creada exitosamente.
        - 422: Si la asignación ya existe o si hay un error en los datos proporcionados.
        """
        data = request.get_json()
        try:
            new_assignment = AssignmentService.create_assignment(data['fk_user_id'], data['fk_habit_id'])
            return make_response(jsonify(
                {'message': f'Habit ID: {new_assignment.fk_habit_id} assigned to user ID: {new_assignment.fk_user_id} successfully'}), 201)
        except ValueError as e:
            # Si la asignación ya existe se responde un mensaje de error con el código 422
            return make_response(jsonify({'message': str(e)}), 422)  
        
    @assignment_ns.doc('get_all_assignments')
    def get(self):
        """
        Obtener todas las asignaciones.
        ---
        Este método permite obtener una lista de todas las asignaciones registradas en la base de datos.

        Responses:
        - 200: Retorna una lista de todas las asignaciones.
        """
        assignments = AssignmentService.get_all_assignments()  
        return marshal(assignments, get_assignment_response_model), 200
    

@assignment_ns.route('/<int:assignment_id>')
@assignment_ns.param('assignment_id', 'ID de la asignación')
class AssignmentDetailResource(Resource):
    @assignment_ns.doc('delete_assignment')
    def delete(self, assignment_id):
        """
        Eliminar una asignación existente.
        ---
        Este método permite eliminar una asignación de hábitos basada en su ID.

        Path Parameters:
        - assignment_id: El ID de la asignación a eliminar.

        Responses:
        - 200: Asignación eliminada exitosamente.
        - 404: Si la asignación no es encontrada.
        """
        try:
            # Llama al servicio para eliminar la asignación
            AssignmentService.delete_assignment(assignment_id)  
            return make_response(jsonify({'message': 'Assignment deleted successfully'}), 200)
        except ValueError as e:
            # Si la asignación no es encontrada, devolvemos un mensaje de error con el código 404
            return make_response(jsonify({'message': str(e)}), 404)

        
@assignment_ns.route('/user/<int:fk_user_id>')
@assignment_ns.param('fk_user_id', 'ID del usuario')
class AssignmentUserResource(Resource):
    @assignment_ns.doc('get_assignments_by_user_id')
    def get(self, fk_user_id):
        """
        Obtener todas las asignaciones de un usuario específico.
        ---
        Este método permite obtener todas las asignaciones asociadas a un usuario basado en su ID.

        Path Parameters:
        - fk_user_id: ID del usuario.

        Responses:
        - 200: Retorna una lista de asignaciones asociadas al usuario.
        - 404: Si no se encuentran asignaciones para el usuario.
        """
        try:
            # Llama al servicio para obtener las asignaciones asociadas al ID del usuario
            assignments = AssignmentService.get_assignments_by_user_id(fk_user_id)  
            return marshal(assignments, get_assignment_response_model), 200
        except ValueError as e:
            # Si las asignaciones no son encontradas, devolvemos un mensaje de error con el código 404
            return make_response(jsonify({'message': str(e)}), 404)
