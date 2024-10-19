from app import db

class Habit(db.Model):
    """
    Modelo que representa un hábito en la aplicación.

    Atributos:
        habit_id (int): Identificador único del hábito (clave primaria).
        habit_name (str): Nombre del hábito.
        time_of_day (Enum): Momento del día en que se realiza el hábito ('mañana', 'tarde' o 'noche').
        habit_status (bool): Estado del hábito (activo o inactivo).
        assignments (list): Lista de asignaciones relacionadas con el hábito.
    """

    __tablename__ = 'habits'  # Nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    habit_id = db.Column(db.Integer, primary_key=True) # Clave primaria
    habit_name = db.Column(db.String(100), nullable=False) # Nombre del hábito
    time_of_day = db.Column(db.Enum('mañana', 'tarde', 'noche'), nullable=True) # Jornada en que se realizará el hábito
    habit_status = db.Column(db.Boolean, default=True, nullable=False) # Status del hábito (activo/inactivo)
    assignments = db.relationship('Assignment', backref='habit', lazy=True)  # Relación con la tabla 'assignments'

    def __init__(self, habit_name, time_of_day):
        """
        Constructor de la clase Habit.

        Args:
            habit_name (str): Nombre del hábito.
            time_of_day (Enum): Momento del día en que se realiza el hábito.
            habit_status (bool): Estado inicial del hábito.
        """
        self.habit_name = habit_name
        self.time_of_day = time_of_day