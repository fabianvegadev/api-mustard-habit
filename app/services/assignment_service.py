from app import db
from app.models.assignment_model import Assignment
from app.models.habit_model import Habit
from app.models.user_model import User
from app.utils.validations import Validations

class AssignmentService:
    """
    Servicio para gestionar las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    relacionadas con las asignaciones de habitos por usuario en la base de datos.
    """
    
    @staticmethod
    def create_assignment(fk_user_id, fk_habit_id):
        """
        Crear una nueva asignación entre un usuario y un hábito.

        Args:
            fk_user_id (int): ID del usuario que realizará el hábito.
            fk_habit_id (int): ID del hábito asignado al usuario.

        Returns:
            Assignment: La asignación recién creada.

        Raises:
            ValueError: Si ya existe una asignación con el mismo usuario y hábito.
        """
        # Verificar que la el id del usuario y del hábitos existan en sus respectivas tablas
        Validations.check_fk_existence(User.user_id, fk_user_id, 'users')
        Validations.check_fk_existence(Habit.habit_id, fk_habit_id, 'habits')

        # Verificar que no exista una asignación duplicada para el mismo usuario y hábito
        Validations.check_data_pair_existence(Assignment.fk_user_id, fk_user_id, Assignment.fk_habit_id, fk_habit_id, 'assignment')

        # Crear una nueva asignación
        new_assignment = Assignment(fk_user_id, fk_habit_id)
        
        # Guardar la nueva asignación en la base de datos
        db.session.add(new_assignment)
        db.session.commit()

        return new_assignment
    
    @staticmethod
    def get_all_assignments():
        """
        Obtener todas las asignaciones de la base de datos.

        Returns:
            List[Assignment]: Lista de todas las asignaciones en la base de datos.
        """
        return Assignment.query.all()
    
    @staticmethod
    def get_assignments_by_user_id(fk_user_id):
        """
        Obtener todas las asignaciones de un usuario por su ID.

        Args:
            fk_user_id (int): El ID del usuario para buscar sus asignaciones.

        Returns:
            List[Assignment]: Lista de asignaciones del usuario.

        Raises:
            ValueError: Si no se encuentran asignaciones para el usuario dado.
        """
        # Buscar asignaciones por el ID del usuario
        assignments = Assignment.query.filter_by(fk_user_id=fk_user_id).all()
        # Verificar si se encontraron asignaciones
        assignments_validated = Validations.check_if_exists(assignments, 'Assignment')
        
        return assignments_validated
    
    @staticmethod
    def delete_assignment(assignment_id):
        """
        Eliminar una asignación existente de la base de datos.

        Args:
            assignment_id (int): ID de la asignación a eliminar.

        Returns:
            None

        Raises:
            ValueError: Si la asignación no se encuentra.
        """
        # Obtener la asignación por su ID
        assignment = AssignmentService.get_assignment_by_assignment_id(assignment_id)
        
        # Eliminar la asignación de la base de datos
        db.session.delete(assignment)
        db.session.commit()

    @staticmethod
    def get_assignment_by_assignment_id(assignment_id):
        """
        Obtener una asignación por su ID.

        Args:
            assignment_id (int): El ID de la asignación a buscar.

        Returns:
            Assignment: La asignación que coincide con el ID proporcionado.

        Raises:
            ValueError: Si la asignación no se encuentra.
        """
        # Buscar la asignación por su ID
        assignment = Assignment.query.filter_by(assignment_id=assignment_id).first()
        # Validar que la asignación exista
        assignment_validated = Validations.check_if_exists(assignment, 'Assignment')
        
        return assignment_validated
