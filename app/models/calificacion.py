from datetime import datetime, timezone
from app import db


class Calificacion(db.Model):
    __tablename__ = "calificaciones"

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey("cursos.id"), nullable=False)
    nota = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    estudiante = db.relationship("Usuario", backref="calificaciones")
    __table_args__ = (db.UniqueConstraint("estudiante_id", "curso_id", name="uq_calificacion"),)