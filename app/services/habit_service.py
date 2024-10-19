from app import db
from app.models.habit_model import Habit
from app.utils.validations import Validations

class HabitService:
    """
    Servicio para gestionar las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    relacionadas con los hábitos en la base de datos.
    """

    @staticmethod
    def create_habit(habit_name, time_of_day):
        """
        Crea un nuevo hábito en la base de datos.

        Args:
            habit_name (str): El nombre del hábito.
            time_of_day (str): El momento del día en que se realiza el hábito. Puede ser "mañana", "tarde" o "noche".

        Returns:
            Habit: El objeto del hábito recién creado.

        Raises:
            ValueError: Si ya existe un hábito con el mismo nombre y momento del día.
        """
        Validations.Check_data_time_of_day(time_of_day)
        # Verificar que no exista un hábito con el mismo nombre y momento del día
        Validations.check_data_pair_existence(Habit.habit_name, habit_name, Habit.time_of_day, time_of_day, 'habit')  
        # Crear un nuevo objeto Habit con los datos proporcionados
        new_habit = Habit(habit_name, time_of_day)
        # Agregar el nuevo hábito a la base de datos y confirmar la transacción
        db.session.add(new_habit)
        db.session.commit()
        # Retornar el hábito creado
        return new_habit

    @staticmethod
    def update_habit(habit_id, habit_name, time_of_day):
        """
        Actualiza un hábito existente en la base de datos.

        Args:
            habit_id (int): El ID del hábito a actualizar.
            new_data (dict): Un diccionario con los nuevos datos del hábito, como 'habit_name' y 'time_of_day'.

        Returns:
            Habit: El hábito actualizado.

        Raises:
            ValueError: Si el hábito no se encuentra o si ya existe un hábito con el mismo nombre y momento del día.
        """
        Validations.Check_data_time_of_day(time_of_day)
        # Validar que no exista otra combinación de nombre y momento del día
        Validations.check_data_pair_existence(Habit.habit_name, habit_name, Habit.time_of_day, time_of_day, 'habit')
        # Buscar el hábito por su ID
        habit = HabitService.get_habit_by_id(habit_id)
        # Actualizar el nombre y el momento del día del hábito
        habit.habit_name = habit_name
        habit.time_of_day = time_of_day
        # Guardar los cambios en la base de datos
        db.session.commit()
        return habit

    @staticmethod
    def delete_habit(habit_id):
        """
        Elimina un hábito existente de la base de datos.

        Args:
            habit_id (int): El ID del hábito a eliminar.

        Raises:
            ValueError: Si el hábito no se encuentra.
        """
        # Obtener el hábito por su ID
        habit = HabitService.get_habit_by_id(habit_id)
        # Eliminar el hábito de la base de datos y confirmar la transacción
        db.session.delete(habit)
        db.session.commit()

    @staticmethod
    def get_all_habits():
        """
        Obtiene todos los hábitos almacenados en la base de datos.

        Returns:
            List[Habit]: Una lista con todos los hábitos registrados.
        """
        return Habit.query.all()
    
    @staticmethod
    def get_habit_by_id(habit_id):
        """
        Obtiene un hábito por su ID.

        Args:
            habit_id (int): El ID del hábito a buscar.

        Returns:
            Habit: El hábito que coincide con el ID proporcionado.

        Raises:
            ValueError: Si el hábito no se encuentra.
        """
        # Buscar el hábito por su ID
        habit = Habit.query.filter_by(habit_id=habit_id).first()
        # Validar que el hábito exista
        habit_validated = Validations.check_if_exists(habit, 'Habit')
        return habit_validated
