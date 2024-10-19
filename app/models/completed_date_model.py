from app import db
from datetime import datetime

class CompletedDate(db.Model):
    """
    Modelo que representa una fecha de finalización de una asignación en la aplicación.

    Atributos:
        completed_date_id (int): Identificador único de la fecha de finalización (clave primaria).
        completed_date (date): Fecha en la que se completó la asignación.
        fk_assignment_id (int): ID de la asignación asociada (clave foránea).
    """

    __tablename__ = 'completed_dates'
    
    completed_date_id = db.Column(db.Integer, primary_key=True)
    completed_date = db.Column(db.Date, default=datetime.now().date(), nullable=False)
    fk_assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.assignment_id'), nullable=False)
    
    def __init__(self, fk_assignment_id, completed_date):
        """
        Constructor de la clase CompletedDate.

        Args:
            fk_assignment_id (int): ID de la asignación asociada a la fecha de finalización.
            completed_date (date): Fecha en la que se completó la asignación.
        """
        self.fk_assignment_id = fk_assignment_id
        self.completed_date = completed_date
