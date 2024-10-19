from app import db
from datetime import datetime

class Assignment(db.Model):
    """
    Modelo que representa una asignación de un hábito a un usuario en la aplicación.

    Atributos:
        assignment_id (int): Identificador único de la asignación (clave primaria).
        created_date (datetime): Fecha y hora en que se creó la asignación.
        assignment_status (bool): Estado de la asignación (True si está activa, False si está inactiva).
        fk_user_id (int): ID del usuario asociado a la asignación (clave foránea).
        fk_habit_id (int): ID del hábito asociado a la asignación (clave foránea).
        completed_dates (list): Lista de fechas en que el usuario ha completado el hábito.
    """

    __tablename__ = 'assignments'

    assignment_id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    assignment_status = db.Column(db.Boolean, default=True, nullable=False)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    fk_habit_id = db.Column(db.Integer, db.ForeignKey('habits.habit_id'), nullable=False)
    completed_dates = db.relationship('CompletedDate', backref='assignment', lazy=True)

    def __init__(self, fk_user_id, fk_habit_id):
        """
        Constructor de la clase Assignment.

        Args:
            fk_user_id (int): ID del usuario asociado a la asignación.
            fk_habit_id (int): ID del hábito asociado a la asignación.
        """
        self.fk_user_id = fk_user_id
        self.fk_habit_id = fk_habit_id
